import json
import random
import asyncio
import logging
import aiofiles
import uvicorn
import traceback
import webbrowser
import numpy as np
from io import BytesIO
from PIL import Image
from aiohttp import ClientSession
from typing import Optional, Union, Any, Tuple
from fastapi import FastAPI, Request, Header, WebSocket, HTTPException, WebSocketDisconnect, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from model import *
from utils.image_operations import magic_wand, numpy_create_mask
from utils.ocr import OCRProxy
from global_control_lib import GlobalControl
from fastapi.staticfiles import StaticFiles



import platform
os_name = platform.system()
if os_name == 'Linux':
    import uvloop
    uvloopp.install()

dev = True
app = FastAPI(docs_url='/docs' if dev else None, rdoc_url= None, debug=dev)
app.mount("/assets", StaticFiles(directory="./assets"), name="assets")

origins = [
    'http://127.0.0.1:7000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

mocr = OCRProxy(dev=dev)

global_control = GlobalControl(logger = logging.getLogger("uvicorn"))

@app.on_event('startup')
async def startup():
    # 清空之前开启的driver
    
    loop = asyncio.get_running_loop()
    await global_control.initialize()
    loop.create_task(global_control.ws_heartbeat())
    loop.create_task(mocr.load_instance(global_control))
    # await mocr.load_instance()
    # webbrowser.open('http://127.0.0.1:7000', autoraise=True)

@app.get('/', response_class=HTMLResponse)
async def index():
    async with aiofiles.open('index.html','r',encoding='utf-8') as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/img/{name}")
async def get_img(name: str):
    content = await global_control.get_img_latest(name, res_type="blob")
    if content is not None:
        return Response(content=content, media_type='image/png')
    return PlainTextResponse(status_code=404, content="File Not Found")

@app.get("/img-thumb/{name}")
async def get_img_thumb(name: str):
    content = global_control.get_img_thumb(name)
    if content is not None:
        return Response(content=content, media_type='image/webp')
    return PlainTextResponse(status_code=404, content="File Not Found")

@app.get('/img-src/{name}')
async def get_img_src(name: str):
    content = global_control.get_img_source(name)
    if content is not None:
        return Response(content=content, media_type='image/webp')
    return PlainTextResponse(status_code=404, content="File Not Found")

@app.post('/api/ready', response_class=JSONResponse)
async def backend_ready(user_agent: str = Header(default="")):
    # loop = asyncio.get_running_loop()
    # async def test(global_control):
    #     await asyncio.sleep(2)
    #     print(global_control.selenium_child_process.exception())
    # loop.create_task(test(global_control))
    return {"success": True, "ready": global_control.backend_check_ready(user_agent)}

@app.post('/api/ready-test')
async def testready():
    await global_control.test_send_msg()
    return {}

@app.post('/api/remove-img', response_class=JSONResponse)
async def remove_img(data: RemoveImgData):
    if data.md5 == "":
        return {"success": False}
    await global_control.remove_img(data.md5)
    return {"success": True}

@app.post('/api/remove-img-all', response_class=JSONResponse)
async def remove_img_all():
    await global_control.remove_img_all()
    return {"success": True}

@app.get('/api/require-img-init', response_class=JSONResponse)
async def require_img_init(ws_uuid: str):
    loop = asyncio.get_running_loop()
    loop.create_task(global_control.ws_send(ws_uuid, {'type': 1, 'desc': '图片更新', 'new_files': global_control.get_img_list()}))
    return {"success": True}

@app.post('/api/file-upload', response_class=JSONResponse)
async def file_upload(file: bytes = File(b''), name: str = Form(...), ftype: str = Form(...), size: int = Form(...), ws_uuid: str = Form(...)):
    try:
        assert size == len(file) and 0 < size < 1024 * 1024 * 20
        test_open = Image.open(BytesIO(file))
        test_open.verify()
        assert test_open.width > 0 and test_open.height > 0
        # 保存文件到本地
        await global_control.register_image(file, name, ftype, (test_open.width, test_open.height))
        loop = asyncio.get_running_loop()
        loop.create_task(global_control.ws_send(ws_uuid, {'type':1, 'desc': '图片更新', 'new_files': global_control.get_img_list()}))
    except Exception as e:
        global_control.logger.warning(traceback.format_exc())
        return {"success": False, "message": "file format error"}
    return {"success": True, "message": "file format ok"}

@app.post('/api/smart-range-detect', response_class=JSONResponse)
async def smart_range_detect(data: SmartDetectData):
    loop = asyncio.get_running_loop()
    # try file exists
    img_arr = await global_control.get_img_latest(data.imageMD5, res_type="array")
    if img_arr is None:
        return {"success": False, "message": "file not found"}
    # real_height, real_width, _ = img_arr.shape
    real_click_x, real_click_y = data.offsetX, data.offsetY
    new_img_arr, text_img = magic_wand(img_arr, real_click_x, real_click_y)
    if text_img is None:
        return {"success": False, "message": "no text found"}
    # else
    global_control.append_new_image_cache(data.imageMD5, new_img_arr)
    japanese_text = mocr(text_img).replace('\r','\n').replace('\n','').strip()
    if japanese_text != "":
        loop.create_task(global_control.ws_send(data.wsUUID, {'type': 2, 'imgMD5': data.imageMD5, 'text': japanese_text, 'carry': {"tokenized": global_control.tokenize(japanese_text)}}))
        loop.create_task(global_control.try_traslate(data.wsUUID, data.imageMD5, japanese_text))
    return {'success': True}

@app.post('/api/manual-range-detect', response_class=JSONResponse)
async def manual_range_detect(data: ManualDetectData):
    if data.moveX < 0 or data.moveY < 0:
        return {'success':0} 
    loop = asyncio.get_running_loop()
    img_arr = await global_control.get_img_latest(data.imageMD5, res_type="array")
    real_height, real_width, _ = img_arr.shape
    mask = numpy_create_mask(data.moveX, data.moveY)
    orn_image_cut = img_arr[max(data.offsetY - 6,0):min(data.offsetY+data.moveY+6, real_height),max(data.offsetX - 6,0):min(data.offsetX+data.moveX+6, real_width), :]

    if orn_image_cut.shape[:2] != mask.shape[:2]:
        limy, limx = min(orn_image_cut.shape[0], mask.shape[0]), min(orn_image_cut.shape[1], mask.shape[1])
        mask = mask[:limy, :limx]
        orn_image_cut = orn_image_cut[:limy, :limx, :]
    orn_image_cut_imgtype = Image.fromarray(orn_image_cut)
    orn_image_cut_copy = np.copy(orn_image_cut).reshape(-1, 3)
    new_image_cut = np.zeros(orn_image_cut.shape)
    avg_color = [0, 0, 0]
    for space in range(3):
        new_image_cut[:, :, space] = np.argmax(np.bincount(orn_image_cut_copy[:, space]))
    # reshape mask
    mask = np.repeat(mask.reshape((*mask.shape, -1)), 3, 2)
    mask_rev = np.ones(mask.shape) - mask 
    new_image_cut = np.round(orn_image_cut * mask_rev + new_image_cut * mask).astype(np.int16)
    new_image_cut = np.minimum(new_image_cut, 255)
    new_image_cut = np.maximum(new_image_cut, 0)

    flag = True
    try:
        img_arr[max(data.offsetY-6,0): data.offsetY-6+new_image_cut.shape[0], max(data.offsetX-6, 0):data.offsetX-6+new_image_cut.shape[1], :] = new_image_cut
    except:
        flag = False
        ...
    # 识图
    japanese_text = mocr(orn_image_cut_imgtype).replace('\r','\n').replace('\n','').strip()
    if japanese_text != "":
        loop.create_task(global_control.ws_send(data.wsUUID, {'type': 2, 'imgMD5': data.imageMD5, 'text': japanese_text, 'carry': {"tokenized": global_control.tokenize(japanese_text)}}))
        loop.create_task(global_control.try_traslate(data.wsUUID, data.imageMD5, japanese_text))

    # 保存输出
    if flag:    
        global_control.append_new_image_cache(data.imageMD5, img_arr)
    return {'success': 1}

@app.post('/api/request-retranslate')
async def request_retranslate(data: ReTranslateData):
    loop = asyncio.get_running_loop()
    if data.wsUUID =='' or data.text == '' or data.imageMD5 == "":
        return {"success": False, "message": "empty request"}
    loop.create_task(global_control.try_traslate(data.wsUUID, data.imageMD5, data.text))
    return {"sucess": True}

@app.post('/api/request-word-translate')
async def request_word_translate(data: ReWordTranslateData):
    loop = asyncio.get_running_loop()
    if data.wsUUID =='' or data.word == '' or data.imageMD5 == "" or data.iid == '':
        return {"success": False, "message": "empty request"}
    loop.create_task(global_control.request_word_translate(data.word, data.wsUUID, data.imageMD5, data.iid))
    return {"success": True}

@app.get('/api/tts-read')
async def tts_read(text: str = ''):
    res = await global_control.read_voice(text)
    return Response(content=res, media_type='audio/mp3')

@app.post('/test/reset')
async def testreset():
    await global_control._test_reset()
    return {'success': True}

@app.websocket('/ws/hold')
async def hold_ws(ws: WebSocket):
    await ws.accept()
    ws_uuid = await ws.receive_text()
    try:
        global_control.append_websocket(ws_uuid, ws)
        while True:
            await ws.send_text(json.dumps({'type': -1}))
            await asyncio.sleep(3) # 仅保持连接，心跳逻辑由外部实现
    except:
        ...
    finally:
        await ws.close()


if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "[%(asctime)s] | %(levelname)s | %(message)s"
    log_config["formatters"]["access"]["fmt"] = "[%(asctime)s] | %(levelname)s | %(message)s"
    uvicorn.run('serve2:app', host="127.0.0.1", port=39921, log_config=log_config, reload=dev)
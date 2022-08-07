import os
import re
import json
import hashlib
import asyncio
import ThreadPoolExecutorPlus
import aiofiles
import async_timeout
import numpy as np
from PIL import Image
from io import BytesIO
from collections import deque
from typing import Union, Tuple, Any, List, Optional
from fastapi import WebSocketDisconnect
from utils.translators import BaiduTranslator, TencentTranslator
from utils.text_to_speech import TTSX3Reader, GoogleTTSReader
from utils.tokenizers import MecebTokenizer, JanomeTokenizer, SudachiTokenizer
from utils.dictionaries import HjDictionary
from ThreadPoolExecutorPlus import ThreadPoolExecutor
from functools import partial
from queue import Queue
from pipeit import *

'''
PIL和numpy都是同步有延迟的，正常操作应该是创建一个线程池负责负载这部分内容。
但是因为图本身算的比较快，大概也就是毫秒级别，实际软件也不是多用户使用，体感上几乎无感，所以就直接写以图省事了。
'''

class GlobalControl:

    def __init__(self, logger):
        self.backend_ready = False
        self.websockets = {}
        self.logger = logger
        self.files = {}
        self.img_arr_caches = {}
        self.img_stream_caches = {}
        self.max_img_cache_size = 5
        # 判断本地是否有tmp目录
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        if not os.path.exists('./misc'):
            os.mkdir('./misc')
        # 获取当前执行文件的绝对路径
        self.path = os.path.abspath(__file__)
        self.tmpdir_path = os.path.join(os.path.dirname(self.path), 'tmp')
        self.miscdir_path = os.path.join(os.path.dirname(self.path), 'misc')
        try:
            baidu_appid, baidu_secretkey, tencent_secretid, tencent_secretkey = Read("secrets.txt").split('\n')
        except:
            baidu_appid, baidu_secretkey, tencent_secretid, tencent_secretkey = '','','',''
        self.thread_pool = ThreadPoolExecutor()
        self.traslators = {
            'baidu': BaiduTranslator(baidu_appid, baidu_secretkey, 'jp', 'zh'),
            'tencent': TencentTranslator(tencent_secretid, tencent_secretkey, 'jp', 'zh')
        }
        self.tts_engines = {
            'ttsx3': TTSX3Reader(),
            'google': GoogleTTSReader()
        }
        self.tokenizers = {
            'meceb': MecebTokenizer(), 
            'janome': JanomeTokenizer(), 
            'sudachi': SudachiTokenizer()
        }
        self.dictionaries = {
            'hj': HjDictionary()
        }
        self.selenium_child_process = None
        self.selenium_queue = Queue()
        self.selenium_resp_future = {}
        self.selenium_req_id = 0
        self.selenium_ready = False

    async def initialize(self):
        # 清空之前的driver
        try:
            os.system("taskkill /f /im chromedriver.exe")
        except:
            ...

        # 测试写入文件权限
        try:
            async with aiofiles.open(os.path.join(self.tmpdir_path, 'test.txt'), 'w') as f:
                await f.write('test')
            os.remove(os.path.join(self.tmpdir_path, 'test.txt'))
            # 初始化：如果tmp目录下存在文件，则清空所有文件
            if os.listdir(self.tmpdir_path):
                for file in os.listdir(self.tmpdir_path):
                    os.remove(os.path.join(self.tmpdir_path, file))
        except Exception as e:
            self.logger.error("初始化失败，没有tmp目录的操作权限，这可能是由于使用超级管理员权限下载和解压导致的，请检查目录权限")


    async def register_image(self, blob: bytes, name: str, ftype: str, img_size: Tuple[int, int]) -> None:
        md5 = hashlib.md5(blob).hexdigest()
        wh_ratio = img_size[0] / img_size[1]
        if img_size[0] >= img_size[1]:
            if img_size[0] >= 240:
                thumbnail_size = (240, int(240 / wh_ratio + 0.5))
            else:
                thumbnail_size = (img_size[0], img_size[1])
        else:
            if img_size[1] >= 240:
                thumbnail_size = (int(240 * wh_ratio + 0.5), 240)
            else:
                thumbnail_size = (img_size[0], img_size[1])
        with BytesIO(blob) as tmp:
            with BytesIO() as tmp2:
                Image.open(tmp).resize(thumbnail_size).save(tmp2, format='webp')
                thumbnail_blob = tmp2.getvalue()
        self.files[md5] = {
            'name': name,
            'ftype': ftype,
            'img_size': img_size,
            'thumbnail_blob': thumbnail_blob,
        }
        async with aiofiles.open(os.path.join(self.tmpdir_path, md5), 'wb') as f:
            await f.write(blob)

    async def get_img_latest(self, name: str, res_type: str="blob") -> Optional[Union[bytes, np.ndarray]]:
        if name not in self.files:
            return None
        if self.img_stream_caches.get(name) is None:
            # 加载图片到缓存中
            async with aiofiles.open(os.path.join(self.tmpdir_path, name), 'rb') as f:
                blob = await f.read()
                self.img_arr_caches[name] = deque([np.array(Image.open(BytesIO(blob)).convert('RGB')),])
            self.files[name]['source_cache'] = blob
            self.refresh_img_stream(name)
        if res_type == "blob":
            return self.img_stream_caches[name]
        elif res_type == "array":
            return self.img_arr_caches[name][-1]
        else:
            raise RuntimeError('res_type参数错误')

    def refresh_img_stream(self, name: str) -> None:
        if name not in self.img_arr_caches:
            self.logger.warning("图片数组缓存载入异常"); return
        arr = self.img_arr_caches[name][-1]
        with BytesIO() as tmp:
            Image.fromarray(arr).save(tmp, format='png')
            self.img_stream_caches[name] = tmp.getvalue()

    def append_websocket(self, ws_uuid: str, ws: 'WebSocket') -> None:
        self.websockets[ws_uuid] = ws

    def remove_websocket(self, ws_uuid: str = '', ws: 'Optional[WebSocket]' = None) -> None:
        if ws_uuid != '':
            del self.websockets[ws_uuid] # 同步函数，未释放ws，通常来说没问题因为会在响应逻辑里关闭
            return
        for key, value in self.websockets.items():
            if value == ws:
                break
        del self.websockets[key]

    async def ws_heartbeat(self):
        while True:
            for ws_uuid, ws in list(self.websockets.items()):
                try:
                    await ws.send_text(json.dumps({'type': 0, 'data': 'heartbeat'}))
                except:
                    self.remove_websocket(ws=ws)
            await asyncio.sleep(3)

    async def ws_send(self, ws_uuid: str, carry: Any) -> bool:
        '''
        ws发送码映射表
        -1: 接收端保活
        0: 心跳
        1: 图片列表更新
        2: 识图原文
        3: 翻译译文
        4: 划词翻译
        '''
        if ws_uuid not in self.websockets:
            return False
        try:
            await self.websockets[ws_uuid].send_text(json.dumps(carry))
            return True
        except WebSocketDisconnect:
            return False
        except:
            return False

    async def ws_send_all(self, carry: Any) -> None:
        for ws_uuid, ws in list(self.websockets.items()):
            try:
                await ws.send_text(json.dumps(carry))
            except:
                ...

    def get_img_list(self) -> List[Tuple[str, str]]:
        res = []
        for md5, value in self.files.items():
            res.append([md5, value['name']])
        return res

    def get_img_thumb(self, name: str) -> bytes:
        if name not in self.files:
            return None
        return self.files[name]['thumbnail_blob']

    def get_img_source(self, name: str) -> bytes:
        if name not in self.files:
            return None
        return self.files[name]['source_cache']

    async def remove_img(self, md5: str) -> None:
        if md5 in self.files:
            del self.files[md5]
        if md5 in self.img_arr_caches:
            del self.img_arr_caches[md5]
        if md5 in self.img_stream_caches:
            del self.img_stream_caches[md5]
        try:
            os.remove(os.path.join(self.tmpdir_path, md5))
        except:
            ...
        try:
            await self.ws_send_all({'type':1, 'desc': '图片更新', 'new_files': self.get_img_list()})
        except:
            ...

    async def remove_img_all(self) -> None:
        self.files.clear()
        self.img_arr_caches.clear()
        self.img_stream_caches.clear()
        # 删除tmp目录下的所有文件
        for file in os.listdir(self.tmpdir_path):
            try:
                os.remove(os.path.join(self.tmpdir_path, file))
            except:
                ...
        try:
            await self.ws_send_all({'type':1, 'desc': '图片更新', 'new_files': self.get_img_list()})
        except:
            ...

    def append_new_image_cache(self, md5: str, img_arr: 'np.array'):
        self.img_arr_caches[md5].append(img_arr)
        while len(self.img_arr_caches[md5]) > self.max_img_cache_size:
            self.img_arr_caches[md5].popleft()
        self.refresh_img_stream(md5)

    async def _test_reset(self):
        self.img_arr_caches.clear()
        self.img_stream_caches.clear()
        for md5 in self.files.keys():
            await self.get_img_latest(md5, 'array')

    async def try_traslate(self, wsUUID: str, imgMD5: str, src_text: str):

        async def fetch_and_send(wsUUID, imgMD5, translator_name):
            success, dst_text = await self.traslators[translator_name].reliable_fetch(src_text)
            await self.ws_send(wsUUID, {'type': 3, 'imgMD5': imgMD5, 'text': dst_text, 'carry': self.traslators[translator_name].carry_info()})

        await asyncio.gather(*[
            fetch_and_send(wsUUID, imgMD5, translator_name) for translator_name in self.traslators.keys() 
        ])

    async def read_voice(self, text: str):
        loop = asyncio.get_running_loop()
        # res = await loop.run_in_executor(self.thread_pool, self.tts_engines['ttsx3'].read, text)
        res = await loop.run_in_executor(self.thread_pool, self.tts_engines['google'].read, text)
        return res

    def tokenize(self, text):
        ...

    def backend_check_ready(self, user_agent:str = ""):
        if self.selenium_child_process is None:
            chrome_agent_ver = re.search("Chrome/[\d]{2,3}\.", user_agent)
            if chrome_agent_ver:
                chrome_agent_ver = chrome_agent_ver.group()
                chrome_agent_ver = chrome_agent_ver[chrome_agent_ver.index('/')+1:chrome_agent_ver.index('.')]
            else:
                chrome_agent_ver = "-1"
            loop = asyncio.get_running_loop()
            self.selenium_child_process = self.thread_pool.submit(self.selenium_thread, loop, self.selenium_queue, chrome_agent_ver)
        return self.backend_ready and self.selenium_ready

    async def request_word_translate(self, word: str="", wsUUID:str="", imgMD5:str="", iid:str=""):
        cur_tid = self.selenium_req_id
        self.selenium_req_id += 1
        fut = self.selenium_resp_future.setdefault(str(cur_tid), asyncio.Future())
        # 添加任务
        self.selenium_queue.put_nowait(("REQ", cur_tid, word))
        try:
            async with async_timeout.timeout(8):
                resp = await fut
                self.logger.info(resp)
        except asyncio.TimeoutError:
            resp = "词典数据获取超时"
        except Exception as e:
            self.logger.warning(f"词典数据获取异常{e}")
            resp = f"词典数据获取异常{e}"
        finally:
            try:
                del self.selenium_resp_future[cur_tid]
            except:
                ...
        await self.ws_send(wsUUID, {'type': 4, 'imgMD5': imgMD5, 'text': resp, 'iid': iid})

    def selenium_response(self, tid: int, resp: str):
        fut = self.selenium_resp_future.get(str(tid))
        if fut is not None:
            try:
                fut.set_result(resp)
                del self.selenium_resp_future[str(tid)]
            except Exception as e:
                self.logger.warning(f"词典数据结果设置异常{e}")
        else:
            # 在没有回调接收的情况下触发，说明未按正常规则使用。
            self.logger.info("回调未被接收")

    def assign_selenium_ready(self):
        self.selenium_ready = True

    def selenium_thread(self, loop, in_q, chrome_agent_ver):
        from selenium import webdriver
        from selenium.webdriver import ChromeOptions
        from selenium.webdriver.chrome.options import Options

        driver_path = os.path.join(self.miscdir_path, f'chromedriver_{chrome_agent_ver}.exe')
        try:
            # 检查本地是否有chromedriver
            if not os.path.exists(driver_path):
                raise Exception('chromedriver not found')
            self.logger.info("无头浏览器启动线程: 发现chromedriver")
        except:
            # 下载chromedriver
            self.logger.info("无头浏览器启动线程: 未发现chromedriver")
            import wget
            from zipfile import ZipFile
            ver_dict = {
                '104': 'https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_win32.zip',
                '103': 'https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_win32.zip',
                '102': 'https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_win32.zip',
                '101': 'https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_win32.zip',
                '100': 'https://chromedriver.storage.googleapis.com/100.0.4896.60/chromedriver_win32.zip',
                '99': 'https://chromedriver.storage.googleapis.com/99.0.4844.51/chromedriver_win32.zip',
                '98': 'https://chromedriver.storage.googleapis.com/98.0.4758.80/chromedriver_win32.zip',
            }
            down_url = ver_dict.get(chrome_agent_ver)
            if down_url is None:
                self.logger.info("无头浏览器启动线程: 未在预置列表里寻找到对应版本的下载地址，可以考虑手动安装。")
                loop.call_soon_threadsafe(self.assign_selenium_ready)
                return
            self.logger.info("无头浏览器启动线程: 开始下载chromedriver")
            wget.download(down_url, os.path.join(self.miscdir_path, f'chromedriver.zip'))
            self.logger.info("无头浏览器启动线程: 下载完成，正在解压。")
            with ZipFile(os.path.join(self.miscdir_path, f'chromedriver.zip'), 'r') as archive:
                try:
                    archive.extractall(path=self.miscdir_path)
                except Exception as e:
                    self.logger.info("无头浏览器启动线程: 尝试解压失败，未知错误")
                    loop.call_soon_threadsafe(self.assign_selenium_ready)
                    return
            os.rename(os.path.join(self.miscdir_path, f'chromedriver.exe'), os.path.join(self.miscdir_path, f'chromedriver_{chrome_agent_ver}.exe'))

        chrome_option = Options()
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-gpu')
        chrome_option.add_argument("window-size=800,600")

        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_option, options=option)
        # driver = webdriver.Chrome()
        working_status = False
        self.logger.info("无头浏览器已启动。")
        try:
            try:
                assert self.dictionaries['hj'].pre_activation(driver)
                loop.call_soon_threadsafe(self.assign_selenium_ready)
                working_status = True
            except:
                self.logger.error("浏览器子线程预激失败。")
                try:
                    driver.quit()
                except:
                    ... 
                return
            while working_status:
                flag, tid, data = in_q.get()
                if flag == 'REQ':
                    try:
                        success, resp = self.dictionaries['hj'].find_explain(driver, self.logger, data)
                    except:
                        resp = '字典内容获取失败'
                    self.logger.debug(resp)
                    loop.call_soon_threadsafe(partial(self.selenium_response, tid, resp))
        finally:
            try:
                driver.quit()
            except:
                ...
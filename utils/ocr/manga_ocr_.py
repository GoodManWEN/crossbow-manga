# from manga_ocr import MangaOcr
import numpy as np
from PIL import Image
import asyncio

class OCRProxy:
    
    def __init__(self, dev: bool = False):
        self.fake = dev
        self.mocr = None

    async def load_instance(self, global_control):
        if self.fake:
            global_control.backend_ready = True
            return False
        await asyncio.sleep(1)
        from manga_ocr import MangaOcr
        self.mocr = MangaOcr()
        test_img = Image.fromarray(np.ones([64, 64, 3]).astype(np.uint8))
        self.mocr(test_img)
        global_control.backend_ready = True
        return True

    def __call__(self, *args,**kwargs):
        if self.fake:
            return "こんにちは。今日もいい天気ですね。"
        if self.mocr is None:
            return "识图引擎还没有准备好哟"
        return self.mocr(*args, **kwargs)
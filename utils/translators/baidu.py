from .base import BaseTranslator
from aiohttp import ClientSession
import json
import random
import hashlib

class BaiduTranslator(BaseTranslator):

    def __init__(self, baidu_appid: str, baidu_secretkey: str, from_lang: str, to_lang: str):
        super(BaiduTranslator, self).__init__(baidu_appid, baidu_secretkey, from_lang, to_lang) 

    def load_status(self, baidu_appid: str, baidu_secretkey: str, from_lang: str, to_lang: str):
        self.appid = baidu_appid
        self.secretkey = baidu_secretkey
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.timeout = 6
        self.entry = 'https://api.fanyi.baidu.com/api/trans/vip/translate'

    async def fetch_logic(self, src_text: str) -> str:
        salt = random.randint(32768, 65535)
        sign = self.appid + src_text + str(salt) + self.secretkey
        sign = hashlib.md5(sign.encode()).hexdigest()
        params = {
            'q': src_text,
            'from': self.from_lang,
            'to': self.to_lang,
            'appid': self.appid,
            'salt': salt,
            'sign': sign
        }
        async with ClientSession() as session:
            async with session.get(self.entry, params=params, timeout=self.timeout) as resp:
                if resp.status == 200:
                    trans_result = json.loads(await resp.text())
                    trans_result = trans_result["trans_result"][0]["dst"]
                    if trans_result != '':
                        return trans_result
                raise RuntimeError(f"http: {resp.status}")

    def carry_info(self):
        return {'translator': '百度', 'translatorColor': '#ffc600'}
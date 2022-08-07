from .base import BaseTranslator
from aiohttp import ClientSession
import json
import random
import hashlib
import time
import hmac
import base64
import binascii

class TencentTranslator(BaseTranslator):

    def __init__(self, tencent_secretid: str, tencent_secretkey: str, from_lang: str, to_lang: str):
        super(TencentTranslator, self).__init__(tencent_secretid, tencent_secretkey, from_lang, to_lang) 

    def load_status(self, tencent_secretid: str, tencent_secretkey: str, from_lang: str, to_lang: str):
        self.secretid = tencent_secretid
        self.secretkey = tencent_secretkey
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.timeout = 6

    async def fetch_logic(self, src_text: str) -> str:
        timeData = str(int(time.time())) 
        nonceData = random.randint(32768, 65535)
        actionData = "TextTranslate" 
        uriData = "tmt.tencentcloudapi.com"
        signMethod="HmacSHA256"
        requestMethod = "GET"
        regionData = "ap-hongkong"
        versionData = '2018-03-21'

        signDictData = {
            'Action' : actionData,
            'Nonce' : nonceData,
            'ProjectId':0,
            'Region' : regionData,
            'SecretId' : self.secretid,
            'SignatureMethod':signMethod,
            'Source': self.from_lang,
            'SourceText': src_text,
            'Target': self.to_lang,
            'Timestamp' : int(timeData),
            'Version':versionData ,
        }

        sign_string = f"{requestMethod}{uriData}/?" + '&'.join(f"{key}={value}" for key, value in signDictData.items())
        digestmod = hashlib.sha256
        hashed = hmac.new(self.secretkey.encode('utf-8'), sign_string.encode('utf-8'), digestmod)
        hashed_b64 = binascii.b2a_base64(hashed.digest())[:-1]
        signDictData["Signature"] = hashed_b64.decode()
        async with ClientSession() as session:
            async with session.get(f'https://{uriData}', params = signDictData) as resp:
                if resp.status == 200:
                    trans_result = json.loads(await resp.text())["Response"]["TargetText"]
                    if trans_result != "":
                        return trans_result
                raise RuntimeError(f"http: {resp.status}")

    def carry_info(self):
        return {'translator': '腾讯', 'translatorColor': '#c200ff'}
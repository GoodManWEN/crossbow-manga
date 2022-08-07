from pydantic import BaseModel

class LectClickData(BaseModel):
    offsetX: int = 0
    offsetY: int = 0
    imageWidth: int = 0
    imageHeight: int = 0

class SmartDetectData(BaseModel):
    offsetX: int = 0
    offsetY: int = 0
    imageMD5: str = ''
    wsUUID: str = ''

class ManualDetectData(BaseModel):
    offsetX: int = 0
    offsetY: int = 0
    moveX: int = 0
    moveY: int = 0
    imageMD5: str = ''
    wsUUID: str = ''


class RemoveImgData(BaseModel):
    md5: str = ''


class ReTranslateData(BaseModel):
    text: str = ''
    wsUUID: str = ''
    imageMD5: str = ''


class ReWordTranslateData(BaseModel):
    word: str = ''
    wsUUID: str = ''
    imageMD5: str = ''
    iid: str = ""
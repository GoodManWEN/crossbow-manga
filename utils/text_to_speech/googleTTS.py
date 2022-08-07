from io import BytesIO

class GoogleTTSReader:

    def __init__(self):
        self.engine = None

    def read(self, text:str) -> bytes:
        if self.engine is None:
            from gtts import gTTS
            self.engine = gTTS 

        if text != '':
            tts = self.engine(text, lang='ja')
            with BytesIO() as tmp:
                tts.write_to_fp(tmp)
                return tmp.getvalue()
        else:
            return b''


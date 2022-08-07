import pyttsx3

class TTSX3Reader:

    def __init__(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        self.choice = None
        
           
    def read(self, text: str) -> bytes:
        if self.choice is None:
            for voice in voices:
                if 'Japanese' in voice.name:
                    break 
            else:
                print(ImportError('ttsx3: 本地不存在日语语音朗读库，请安装Windows日语语言包。'))
                return b''
            self.choice = voice
        engine = pyttsx3.init()
        engine.setProperty("voice", self.choice.id) 
        engine.setProperty('rate', 100) 
        engine.setProperty('volume',1.0)
        if text != "":
            engine.say(text)
            engine.runAndWait()
        engine.stop()
        return b""
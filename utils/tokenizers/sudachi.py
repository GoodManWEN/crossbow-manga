from .base_tokenizer import BaseTokenizer
from collections.abc import Iterable

class SudachiTokenizer(BaseTokenizer):

    def __init__(self):
        super().__init__()

    def parse(self, text: str):
        if self.engine is None:
            from sudachipy import tokenizer
            from sudachipy import dictionary
            self.engine = dictionary.Dictionary().create()
            self.mode = tokenizer.Tokenizer.SplitMode.B
        return self.format_results(self.engine.tokenize(text, self.mode))

    def format_results(self, pipe: Iterable):
        lst = []
        for i in pipe:
            tk = '未知'
            for tk in i.part_of_speech():
                if '詞' in tk or '号' in tk:
                    break 
            lst.append((i.surface(), tk))
        return lst
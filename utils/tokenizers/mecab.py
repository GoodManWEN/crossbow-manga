from .base_tokenizer import BaseTokenizer
from collections.abc import Iterable


class MecebTokenizer(BaseTokenizer):

    def __init__(self):
        super().__init__()

    def parse(self, text: str):
        if self.engine is None:
            from MeCab import Tagger
            self.engine = Tagger()

        parsed = self.engine.parse(text)
        return self.format_results(parsed.splitlines())

    def format_results(self, pipe: Iterable):
        pieces = []
        for i in pipe[:-1]:
            i = i.split()
            t = ""
            for t in i[::-1]:
                if '詞' in t or '記号' in t: 
                    break 
            if '-' in t:
                t = t[:t.index('-')]
            pieces.append((i[0], t if t != '' else "未知"))
        return pieces

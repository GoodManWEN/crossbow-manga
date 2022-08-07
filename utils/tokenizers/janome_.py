from .base_tokenizer import BaseTokenizer
from collections.abc import Iterable
import re

class JanomeTokenizer(BaseTokenizer):

    def __init__(self):
        super().__init__()
        self.re_searcher = re.compile('.{1,5}?(詞|号)')

    def parse(self, text: str):
        if self.engine is None:
            from janome.tokenizer import Tokenizer
            self.engine = Tokenizer()
        return self.format_results(self.engine.tokenize(text))

    def format_results(self, pipe: Iterable):
        lst = []
        for i in pipe:
            res = str(i)
            if '\t' in res:
                word, bias = res[:res.index('\t')], res[res.index('\t')+1:]
                tk = self.re_searcher.search(bias)
                if tk:
                    lst.append((word, tk.group()))
                else:
                    lst.append((word, '未知'))
            else:
                lst.append(("", '未知'))
        return lst
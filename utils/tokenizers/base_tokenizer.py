from collections.abc import Iterable 
from abc import abstractmethod

class BaseTokenizer:

    def __init__(self):
        self.engine = None 

    @abstractmethod
    def parse(self, text: str):
        ...

    @abstractmethod
    def format_results(self, pipe: Iterable):
        ...

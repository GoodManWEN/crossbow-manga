from abc import abstractmethod
import traceback
import sys
from typing import Union

class BaseTranslator:

    def __init__(self, *args, **kwargs):
        self.load_status(*args, **kwargs)

    @abstractmethod
    def load_status(self):
        raise NotImplementedError()

    @abstractmethod
    async def fetch_logic(self):
        raise NotImplementedError()

    async def reliable_fetch(self, *args, **kwargs) -> Union[bool, str]:
        fail_count = 0
        while fail_count < 2:
            try:
                res = await self.fetch_logic(*args, **kwargs)
                if res == '':
                    res = '--翻译API错误--'
                return True, res
            except Exception as e:
                raise e
                traceback.format_exc()
                fail_count += 1
                if fail_count == 2:
                    return False, '--翻译API错误--'


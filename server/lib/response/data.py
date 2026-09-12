'''
Response data abstract definition
@author shuohui liu
@date 11 Sep 2026
'''

from pydantic import BaseModel

class Data(BaseModel):
    def to_dict(self) -> dict:
        return self.__dict__
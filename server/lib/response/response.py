'''
Response definition, used to do data response from http services to restful api
@author shuohui liu
@date 11 Sep 2026
'''

from exception import ServErrorCode, wrap_code
from pydantic import BaseModel

class Response(BaseModel):
    code: str
    message: str
    detail: str

    def is_success(self) -> bool:
        return ServErrorCode.Success.value[0] == self.code

    def __init__(self, code:ServErrorCode, detail:str = ""):
        serv_code = wrap_code(code)
        print(f'serv_code: {serv_code}')
        
        self.code = serv_code[0]
        self.message = serv_code[1]
        self.detail = detail
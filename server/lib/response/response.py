'''
Response definition, used to do data response from http services to restful api
@author shuohui liu
@date 11 Sep 2026
'''

from exception import ServErrorCode, wrap_code
from pydantic import BaseModel

class Response(BaseModel):
    code: str = ''
    message: str = ''
    detail: str = ''

    def is_success(self) -> bool:
        return ServErrorCode.Success.value[0] == self.code

    def build(self, code: str = '', message: str = '', detail: str = ""):
        self.code = code
        self.message = message
        self.detail = detail
        return self

def error_to_response(error: ServErrorCode, detail: str = '') -> Response:
    code, message = wrap_code(error)
    return Response().build(code, message, detail)
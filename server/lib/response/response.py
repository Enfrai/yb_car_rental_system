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

    def __init__(self, code: str, message: str = '', detail: str = ""):
        super().__init__(
            code=code,
            message=message,
            detail=detail,
        )

def error_to_response(error: ServErrorCode, detail: str = '') -> Response:
    code, message = wrap_code(error)
    return Response(code, message, detail)
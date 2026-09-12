'''
HTTP response definition, used to do data response from FE to BE
@author shuohui liu
@date 11 Sep 2026
'''

from .response import Response
from .data import Data
from exception import ServErrorCode, wrap_code
from typing import Generic, TypeVar, Optional, Union

T = TypeVar('T')

class HTTPResponse(Response):
    data: Optional[T] = None

    def build(self, code:str = '', message:str = '', detail:str = "", data: Generic[T] = None):
        super().build(code if code else "", message if message else "", detail if detail else "");
        self.data = data if data else {}
        return self


def exception_to_http_response(e: Exception) -> HTTPResponse:
    d = e.__dict__
    code = d.get('code', None)
    message = d.get('message', None)
    detail = d.get('detail', None)
    return HTTPResponse().build(
        code if code else ServErrorCode.CommonError.value[0],
        message if message else ServErrorCode.CommonError.value[1],
        detail if detail else f'{e}'
    )

def exception_to_response(e: Exception) -> Response:
    d = e.__dict__
    code = d.get('code', None)
    message = d.get('message', None)
    detail = d.get('detail', None)
    return Response().build(
        code if code else ServErrorCode.CommonError.value[0],
        message if message else ServErrorCode.CommonError.value[1],
        detail if detail else f'{e}'
    )

def error_to_http_response(error: ServErrorCode, detail: str = '', data = None) -> HTTPResponse:
    code, message = wrap_code(error)
    return HTTPResponse().build(code, message, detail, data)
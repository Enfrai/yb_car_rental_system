'''
HTTP response definition, used to do data response from FE to BE
@author shuohui liu
@date 11 Sep 2026
'''

from .response import Response
from .data import Data
from exception import ServErrorCode, wrap_code

class HTTPResponse(Response):
    data: Data = None

    def __init__(self, code:str, message:str, detail:str = "", data:Data = None, **kwargs):
        super().__init__(
            code=code if code else "", 
            message=message if message else "", 
            detail=detail if detail else "", 
            data=data if data else {}, 
            **kwargs
        )


def exception_to_http_response(e: Exception) -> HTTPResponse:
    d = e.__dict__
    code = d.get('code', None)
    message = d.get('message', None)
    detail = d.get('detail', None)
    return HTTPResponse(
        code if code else ServErrorCode.CommonError.value[0],
        message if message else ServErrorCode.CommonError.value[1],
        detail if detail else f'{e}'
    )

def exception_to_response(e: Exception) -> Response:
    d = e.__dict__
    code = d.get('code', None)
    message = d.get('message', None)
    detail = d.get('detail', None)
    return Response(
        code if code else ServErrorCode.CommonError.value[0],
        message if message else ServErrorCode.CommonError.value[1],
        detail if detail else f'{e}'
    )

def error_to_http_response(error: ServErrorCode, detail: str = '', data = None) -> HTTPResponse:
    code, message = wrap_code(error)
    return HTTPResponse(code, message, detail, data)
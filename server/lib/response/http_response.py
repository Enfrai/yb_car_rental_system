'''
HTTP response definition, used to do data response from FE to BE
@author shuohui liu
@date 11 Sep 2026
'''

from .response import Response
from .data import Data

class HTTPResponse(Response):
    data: Data = None

    def __init__(self, code:str, message:str, detail:str = "", data:Data = None):
        super().__init__(code, message, detail)
        self.data = data

    def to_dict(self) -> dict:
        return {
            "code": self.code if self.code is not None else "",
            "message": self.message if self.message is not None else "",
            "detail": self.detail if self.detail is not None else "",
            "data": self.data.to_dict() if self.data is not None else {}
        }

    def __str__(self):
        return str(self.to_dict())

def exception_to_http_response(e: Exception) -> HTTPResponse:
    d = dict(f'{e}')
    code = d.get('code', None)
    message = d.get('message', None)
    detail = d.get('detail', None)
    return HTTPResponse(
        code if code else '',
        message if message else '',
        detail if detail else d,
    )

def exception_to_response(e: Exception) -> Response:
    d = dict(f'{e}')
    code = d.get('code', None)
    message = d.get('message', None)
    detail = d.get('detail', None)
    return Response(
        code if code else '',
        message if message else '',
        detail if detail else d,
    )
from .codes import ServErrorCode

class DBExeError(ValueError):
    code: ServErrorCode

    def __init__(self, code: ServErrorCode, *args):
        self.code = code
        super().__init__(*args)

    def __str__(self):
        if self.code is None:
                return super().__str__()
        else:
            return '{' + f'"code": {self.code.value[0]}, "message": {self.code.value[1]}, "detail": {super().__str__()}' + '}'
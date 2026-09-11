'''
car error definition
@author shuohui liu
@date 10 Sep 2026
'''

from .codes import ServErrorCode

class CarError(ValueError):
    code: ServErrorCode

    def __init__(self, code: ServErrorCode, *args):
            self.code = code
            super().__init__(*args)
    
    def __str__(self):
        if not self.code:
                return super().__str__()
        else:
            return '{' + f'"code": {self.code.value[0]}, "message": {self.code.value[1]}, "detail": {super().__str__()}' + '}'
'''
Service error definition
@author shuohui liu
@date 10 Sep 2026
'''
from enum import Enum

class ServErrorCode(Enum):
    Success = ("0", "")
    ExecuteError = ("1", "Inner Execute Error")
    CommonError = ('2', 'Common error')
    UserExist = ("1001", "User already exists")
    UserLoginFailed = ("1002", "Wrong password or email")
    UserNotExist = ("1003", "User not exist")
    UserInfoMissed = ("1004", "Necessary user info missed")
    UserRegFailed = ("1005", "User register failed")
    UserInfoWrong = ("1006", "User info wrong")
    UserInfoUpdateFailed = ("1007", "User info update failed")
    UserNoAdminExist = ("1008", "No admin user exist")
    CarNotExist = ("2001", "Car not exist")
    CarInfoMissed = ("2002", "Necessary car information missed")
    CarRegisterFailed = ("2003", "Car register failed")
    CarSearchFailed = ("2004", "Car search failed")
    OrderNotExist = ("3001", "Order not exist")
    OrderInfoMissed = ("3002", "Necessary order info missed")
    OrderGenFailed = ("3003", "Book an order failed")
    OrderSearchError = ("3004", "Searching with missed info")


def wrap_code(code: ServErrorCode) -> tuple:
    if not code: 
        return None

    return (f'-{code.value[0]}', code.value[1])
'''
User model definition
@author shuohui liu
@date 10 Sep 2026
'''

from lib import Response, error_to_response
from db import UserTable, Columns
from lib import email_is_valid, Logger
from exception import ServErrorCode
from enum import Enum

class Role(Enum):
    ADMIN = 0x1
    CUSTOMER = 0x10

def str_to_role(r: str) -> Role:
    return Role.ADMIN if r == 'admin' else Role.CUSTOMER if r == 'customer' else None

class User:
    user_id: int
    username: str
    password: str   # login key
    email: str      # login key
    role: int       # 

    def __init__(self):
        pass

    def update(self, user_id: int) -> Response:
        '''
        update user info by user_id
        '''
        user = UserTable()
        try:
            success = user.update(user_id, self.username, self.email, 
                        self.password, self.role & Role.ADMIN.value != 0, 
                        self.role & Role.CUSTOMER.value != 0)

            if not success:
                return error_to_response(ServErrorCode.UserInfoUpdateFailed, 'Update user info failed.')

            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            return error_to_response(ServErrorCode.UserInfoUpdateFailed, 'Update user info failed.')


    def register(self, username:str, password:str, email:str, role:int = 0) -> Response:
        '''
        To register a new user.
        '''

        Logger().debug(f"[model] register user: username: {username}, password: {password}, email: {email}, role: {role}")

        if not username or not password or not email or role == 0 or not email_is_valid(email):
            return error_to_response(ServErrorCode.UserInfoMissed, "Have missed info to login.")

        self.username = username
        self.password = password
        self.email = email

        user = UserTable()

        try:
            success = user.insert(username, email, password, role & Role.ADMIN.value != 0, role & Role.CUSTOMER.value != 0)
            if not success:
                Logger().debug("[model] register user: fail")
                return error_to_response(ServErrorCode.UserRegFailed, "Register user failed.")

            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            Logger().debug(f"[model] register user: exception: {e}")
            return error_to_response(ServErrorCode.UserRegFailed, "Register user failed.")

    def search_by_email_or_id(self, email:str = None, user_id: str = None, accept_null: bool = False) -> Response:
        user = UserTable()

        Logger().debug(f"[model] search_by_email_or_id: email: {email}, user_id: {user_id}")

        try:
            resp = {}
            if user_id:
                resp = user.search_by_id(user_id)
            elif email:
                resp = user.search_by_email(email)
            else:
                Logger().debug("[model] search_by_email_or_id: failed >> user_id or email is null")
                return error_to_response(ServErrorCode.UserInfoMissed)

            if not resp:
                if accept_null:
                    Logger().debug(f"[model] search_by_email_or_id: success but return success, because of accept_null: {accept_null}")
                    return error_to_response(ServErrorCode.Success)
                else:
                    Logger().debug(f"[model] search_by_email_or_id: fail for not user found")
                    return error_to_response(ServErrorCode.CommonError)

            self.user_id = resp[Columns.ID.value]
            self.username = resp[Columns.USERNAME.value]
            self.email = resp[Columns.EMAIL.value]

            self.role = 0
            is_admin = resp[Columns.IS_ADMIN.value]
            if is_admin:
                self.role |= Role.ADMIN.value

            is_customer = resp[Columns.IS_CUSTOMER.value]
            if is_customer:
                self.role |= Role.CUSTOMER.value

            Logger().debug("[model] search_by_email_or_id: user_info: ", self.__dict__)

            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            Logger().debug(f"[model] search_by_email_or_id: fail: {e}")
            return error_to_response(ServErrorCode.CommonError)

    def login(self, email:str, password:str) -> Response:
        '''
        The action to login a user by email and password.
        @return dictionary with keys: code, message, detail, data: {}
        '''

        Logger().debug(f"[model] login: email: {email}, password: {password}")

        if not email or not password or not email_is_valid(email):
            return error_to_response(ServErrorCode.UserInfoMissed, "WRONG login info.")

        user = UserTable()

        try:
            data = user.search_by_email_and_password(email, password)

            self.user_id = data.get(Columns.ID.value, None)
            if not self.user_id:
                return error_to_response(ServErrorCode.UserNotExist, "Login Failed.")

            Logger().debug(f"[model] login: parsing parameters...")

            self.username = data[Columns.USERNAME.value]
            self.email = data[Columns.EMAIL.value]

            self.role = 0
            is_admin = data[Columns.IS_ADMIN.value]
            if is_admin:
                self.role |= Role.ADMIN.value

            is_customer = data[Columns.IS_CUSTOMER.value]
            if is_customer:
                self.role |= Role.CUSTOMER.value

            Logger().debug(f"[model] login: parsing parameters : {self.__dict__}")

            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            Logger().debug(f"[model] login: exception: {e}")
            return error_to_response(ServErrorCode.CommonError)


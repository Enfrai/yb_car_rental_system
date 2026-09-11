'''
User model definition
@author shuohui liu
@date 10 Sep 2026
'''

from lib import Response
from db import UserTable, Columns
from lib import email_is_valid
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
                return Response(ServErrorCode.UserInfoUpdateFailed, 'Update user info failed.')

            return Response(ServErrorCode.Success)
        except Exception as e:
            return Response(ServErrorCode.UserInfoUpdateFailed, 'Update user info failed.')


    def register(self, username:str, password:str, email:str, role:int = 0) -> Response:
        '''
        To register a new user.
        '''

        if not username or not password or not email or role == 0 or not email_is_valid(email):
            return Response(ServErrorCode.UserInfoMissed, "Have missed info to login.")

        self.username = username
        self.password = password
        self.email = email

        user = UserTable()

        try:
            success = user.insert(username, email, password, role & Role.ADMIN.value != 0, role & Role.CUSTOMER.value != 0)
            if not success:
                return Response(ServErrorCode.UserRegFailed, "Register user failed.")

            return Response(ServErrorCode.Success)
        except Exception as e:
            return Response(ServErrorCode.UserRegFailed, "Register user failed.")

    def search_by_email_or_id(self, email:str = None, user_id: str = None) -> Response:
        user = UserTable()

        try:
            resp = {}
            if user_id:
                resp = user.search_by_id(user_id)
            elif email:
                resp = user.search_by_email(email)
            else:
                return Response(ServErrorCode.UserInfoMissed)

            self.user_id = resp[Columns.ID]
            self.username = resp[Columns.USERNAME]
            self.email = resp[Columns.EMAIL]

            self.role = 0
            is_admin = resp[Columns.IS_ADMIN]
            if is_admin:
                self.role |= Role.ADMIN.value

            is_customer = resp[Columns.IS_CUSTOMER]
            if is_customer:
                self.role |= Role.CUSTOMER.value

            return Response(ServErrorCode.Success)
        except Exception as e:
            return Response(ServErrorCode.CommonError)

    def login(self, email:str, password:str) -> Response:
        '''
        The action to login a user by email and password.
        @return dictionary with keys: code, message, detail, data: {}
        '''

        if not email or not password or not email_is_valid(email):
            return Response(ServErrorCode.UserInfoMissed, "WRONG login info.")

        user = UserTable()

        try:
            dict = user.search_by_email_and_password(email, password)

            self.user_id = dict.get(Columns.ID, None)
            if not self.user_id:
                return Response(ServErrorCode.UserNotExist, "Login Failed.")

            self.username = dict[Columns.USERNAME]

            self.role = 0
            is_admin = dict[Columns.IS_ADMIN]
            if is_admin:
                self.role |= Role.ADMIN.value

            is_customer = dict[Columns.IS_CUSTOMER]
            if is_customer:
                self.role |= Role.CUSTOMER.value

            return Response(ServErrorCode.Success)
        except Exception as e:
            return Response(ServErrorCode.CommonError)


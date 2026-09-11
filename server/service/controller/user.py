from pydantic import BaseModel, Field
from service.model import User
from lib import Response, HTTPResponse, exception_to_http_response
from service.view import UserInfoData
from service.model import Role, str_to_role
from exception import ServErrorCode
from lib import email_is_valid

class UserLoginRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

class UserRegisterRequest(UserLoginRequest):
    username: str = Field(...)
    role: str = Field(...)
    auto_login: bool = Field(...)

class UserUpdateRequest(UserRegisterRequest):
    user_id: str = Field(...)

class UserSearchRequest(BaseModel):
    user_id: int = Field(...)

class UserController:
    def update(self, req: UserUpdateRequest) -> HTTPResponse:
        '''
        udpate user info, user_id is necessary.
        '''
        try: 
            if not req.user_id:
                return HTTPResponse(ServErrorCode.UserInfoMissed, "user_id is necessary but missed.")

            user_id = int(req.user_id)

            user = User()
            user.username = req.username
            user.email = req.email
            user.password = req.password
            user.role = str_to_role(req.role)

            resp = user.update(req.user_id)
            if resp.is_success():
                s_req = UserSearchRequest()
                s_req.user_id = user_id
                resp = self.search(req)
                return HTTPResponse(resp.code, resp.message, resp.detail, resp.data)

            return HTTPResponse(resp.code, resp.message, resp.detail)
        except ValueError:
            return HTTPResponse(ServErrorCode.UserInfoWrong, "WRONG user_id is provided.")

    def search(self, req: UserSearchRequest) -> HTTPResponse:
        '''
        search a user info by user_id
        '''

        try:
            if not req.user_id:
                return HTTPResponse(ServErrorCode.UserInfoMissed, "user_id is necessary but missed.")

            user_id = int(req.user_id)
            user = User()
            resp = user.search_by_email_or_id(user_id=user_id)
            data = None

            if resp.is_success():
                data = UserInfoData(user.user_id, user.username, user.email, 
                                    user.role & Role.ADMIN.value != 0,
                                    user.role & Role.CUSTOMER.value != 0)

            return HTTPResponse(resp.code, resp.message, resp.detail, data)
        except ValueError:
            return HTTPResponse(ServErrorCode.UserInfoWrong, "WRONG user_id is provided.")


    def login(self, req: UserLoginRequest) -> HTTPResponse:
        user = User()

        resp = user.login(req.email, req.password)
        if resp.is_success():
            role = user.role
            data = UserInfoData(user.user_id, user.username, user.email, 
                                None if not role else role & Role.ADMIN != 0, 
                                None if not role else role & Role.CUSTOMER != 0)

        return HTTPResponse(resp.code, resp.message, resp.detail, data)

    def register(self, req: UserRegisterRequest) -> HTTPResponse:
        user = User()
        resp = user.search_by_email_or_id(req.email)
        if not resp.is_success():
            return HTTPResponse(resp.code, resp.message, resp.detail)

        if user.user_id:
            return HTTPResponse(ServErrorCode.UserRegFailed, 'User already existed.')

        if not req.role or not req.username or req.password or req.email:
            return HTTPResponse(ServErrorCode.UserInfoMissed, 'User info missed.')

        if req.role == 'admin':
            role = Role.ADMIN
        elif req.role == 'customer':
            role = Role.CUSTOMER
        else:
            return HTTPResponse(ServErrorCode.UserRegFailed, 'WRONG role.')

        if not email_is_valid(req.email):
            return HTTPResponse(ServErrorCode.UserRegFailed, 'WRONG email')

        if len(req.username) <= 0:
            return HTTPResponse(ServErrorCode.UserRegFailed, 'WRONG username')

        if len(req.password) <= 0:
            return HTTPResponse(ServErrorCode.UserRegFailed, 'WRONG password')

        user = User()
        resp = user.register(req.username, req.password, req.email, role)
        if resp.is_success():
            if req.auto_login:
                return self.login(req)
            else:
                HTTPResponse(ServErrorCode.Success)

        return HTTPResponse(resp.code, resp.message, resp.detail)
            

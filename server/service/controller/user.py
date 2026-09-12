from pydantic import BaseModel, Field
from service.model import User
from lib import Response, HTTPResponse, exception_to_http_response, error_to_http_response
from service.view import UserInfoData
from service.model import Role, str_to_role
from exception import ServErrorCode
from lib import email_is_valid, Logger

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
                return error_to_http_response(ServErrorCode.UserInfoMissed, "user_id is necessary but missed.")

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
                return HTTPResponse().build(resp.code, resp.message, resp.detail, resp.data)

            return HTTPResponse().build(resp.code, resp.message, resp.detail)
        except ValueError:
            return error_to_http_response(ServErrorCode.UserInfoWrong, "WRONG user_id is provided.")
        except Exception as e:
            return exception_to_http_response(e)

    def search(self, req: UserSearchRequest) -> HTTPResponse:
        '''
        search a user info by user_id
        '''

        try:
            if not req.user_id:
                return error_to_http_response(ServErrorCode.UserInfoMissed, "user_id is necessary but missed.")

            user_id = int(req.user_id)
            user = User()
            resp = user.search_by_email_or_id(user_id=user_id)
            data = None

            if resp.is_success():
                data = UserInfoData().build(user.user_id, user.username, user.email, 
                                    user.role & Role.ADMIN.value != 0,
                                    user.role & Role.CUSTOMER.value != 0)

            return HTTPResponse().build(resp.code, resp.message, resp.detail, data)
        except ValueError:
            return error_to_http_response(ServErrorCode.UserInfoWrong, "WRONG user_id is provided.")
        except Exception as e:
            return exception_to_http_response(e)


    def login(self, req: UserLoginRequest) -> HTTPResponse:
        user = User()

        Logger().debug("[controller] login: ", req.__dict__)

        try:
            resp = user.login(req.email, req.password)
            data = None

            if resp.is_success():
                role = user.role
                data = UserInfoData().build(user.user_id, user.username, user.email, 
                                    None if not role else role & Role.ADMIN.value != 0, 
                                    None if not role else role & Role.CUSTOMER.value != 0)

                Logger().debug(f"[controller] login: success >> {data.__dict__}")
            else:
                Logger().debug(f"[controller] login: fail >> {resp.__dict__}")
            
            r = HTTPResponse().build(resp.code, resp.message, resp.detail, data)
            Logger().debug(f"[controller] login: success >> response: {r.model_dump_json()}")
            return r
        except Exception as e:
            Logger().debug(f"[controller] login: exception >> {e}")
            return exception_to_http_response(e)

    def register(self, req: UserRegisterRequest) -> HTTPResponse:
        Logger().debug("[controller] register user: ", req.__dict__)
        
        user = User()
        resp = user.search_by_email_or_id(req.email, accept_null=True)
        if not resp.is_success():
            return HTTPResponse().build(resp.code, resp.message, resp.detail)

        if user.is_valid():
            return error_to_http_response(ServErrorCode.UserRegFailed, 'User already existed.')

        if not req.role or not req.username or not req.password or not req.email:
            return error_to_http_response(ServErrorCode.UserInfoMissed, 'User info missed.')

        if req.role == 'admin':
            role = Role.ADMIN.value
        elif req.role == 'customer':
            role = Role.CUSTOMER.value
        else:
            return error_to_http_response(ServErrorCode.UserRegFailed, 'WRONG role.')

        if not email_is_valid(req.email):
            return error_to_http_response(ServErrorCode.UserRegFailed, 'WRONG email')

        if len(req.username) <= 0:
            return error_to_http_response(ServErrorCode.UserRegFailed, 'WRONG username')

        if len(req.password) <= 0:
            return error_to_http_response(ServErrorCode.UserRegFailed, 'WRONG password')

        user = User()
        
        resp = user.register(req.username, req.password, req.email, role)
        if resp.is_success():
            if req.auto_login:
                Logger().debug("[controller] register user >> auto login ...") 
                return self.login(req)
            else:
                Logger().debug("[controller] register user: success") 
                error_to_http_response(ServErrorCode.Success)

        Logger().debug("[controller] register user: fail") 
        return HTTPResponse().build(resp.code, resp.message, resp.detail)
            

from lib import Data
from lib import safe_string

class UserInfoData(Data):
    user_id: str
    username: str
    email: str      # login key
    is_admin: bool
    is_customer: bool

    def __init__(self, user_id: int, username:str, email: str, is_admin: bool, is_customer: bool):
        user_id = f'{user_id}' if user_id else ''
        username = safe_string(username)
        email = safe_string(email)
        self.is_customer = is_customer
        self.is_admin = is_admin

    def to_dict(self) -> dict:
        return self.__dict__
        
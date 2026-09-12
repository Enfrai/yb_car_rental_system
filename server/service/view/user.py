from lib import Data
from lib import safe_string

class UserInfoData(Data):
    user_id: str = None
    username: str = None
    email: str = None      # login key
    is_admin: bool = None
    is_customer: bool = None

    def build(self, user_id, username:str, email: str, is_admin: bool, is_customer: bool):
        self.user_id = f'{user_id}' if user_id else user_id if isinstance(user_id, str) else ''
        self.username = safe_string(username)
        self.email = safe_string(email)
        self.is_admin = is_admin
        self.is_customer = is_customer
        return self

        
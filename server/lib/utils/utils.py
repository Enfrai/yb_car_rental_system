import re
import time
from enum import Enum

class SortOrder(Enum):
    DESC = 'DESC'
    ASC = 'ASC'

def email_is_valid(email: str) -> bool:
    if not email:
        return False

    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

def safe_string(v:str, default:str = '') -> str:
    return v if v else default

def gen_unique_id() -> int:
    return time.time_ns()
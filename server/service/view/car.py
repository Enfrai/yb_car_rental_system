from lib import Data
from lib import safe_string

class CarIdData(Data):
    car_id: str

    def __init__(self, car_id: int):
        self.car_id = f'{car_id}' if car_id else ''

    def to_dict(self) -> dict:
        return self.__dict__
        
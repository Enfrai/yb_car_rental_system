from lib import Data
from lib import safe_string

class CarIdData(Data):
    car_id: str

    def __init__(self, car_id: int):
        self.car_id = f'{car_id}' if car_id else ''

    def to_dict(self) -> dict:
        return self.__dict__

class CarInfoData(Data):
    car_id: str
    user_id: str
    make: str
    model: str
    year: int
    mileage: int
    rent_status: int
    min_rent_period: int
    max_rent_period: int
    
    def build(self, car_id: int, 
                user_id: int,
                make: str,
                model: str,
                year: int,
                mileage: int,
                rent_status: int,
                min_rent_period: int,
                max_rent_period: int):
        self.car_id = f'{car_id}' if car_id else ''
        self.user_id = f'{user_id}' if user_id else ''
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.rent_status = rent_status
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period

        return self

    def to_dict(self) -> dict:
        return self.__dict__

class CarInfoList(Data):
    cars: list[CarInfoData] = []

    def build(self, data: list[CarInfoData] = []):
        self.cars = data
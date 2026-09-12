from lib import Data
from lib import safe_string

class CarIdData(Data):
    car_id: str

    def __init__(self, car_id, **kwargs):
        super().__init__(
            car_id = f'{car_id}' if car_id else car_id if isinstance(car_id, str) else '',
            **kwargs
        )


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
    
    def __init__(self, car_id, 
                user_id,
                make: str,
                model: str,
                year: int,
                mileage: int,
                rent_status: int,
                min_rent_period: int,
                max_rent_period: int,
                **kwargs):
        super().__init(
            car_id = f'{car_id}' if car_id else '',
            user_id = f'{user_id}' if user_id else '',
            make = make,
            model = model,
            year = year,
            mileage = mileage,
            rent_status = rent_status,
            min_rent_period = min_rent_period,
            max_rent_period = max_rent_period,
            **kwargs
        )


class CarInfoList(Data):
    cars: list[CarInfoData] = []

    def __init__(self, cars: list[CarInfoData], *args, **kwargs):
        super().__init(
            cars = cars if cars else [],
            *args, **kwargs
        )
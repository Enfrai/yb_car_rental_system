'''
Car model definition
@author shuohui liu
@date 10 Sep 2026
'''

from db import table_car as car
from exception import ServErrorCode
from lib import Response, error_to_response, Logger

S_VALID = 'available'   # 0
S_IN_RENT = 'in_rent'     # 1
S_PENDDING = 'pendding'   # 2
S_INVALID = 'not_available'   # -1

def car_status_from_str(s: str) -> int:
    if S_VALID == s:
        return car.Status.VALID.value
    elif S_IN_RENT == s:
        return car.Status.IN_RENT.value
    elif S_PENDDING == s:
        return car.Status.PENDDING.value
    elif S_INVALID == s: 
        return car.Status.INVALID.value
    else: 
        return None
    

def car_status_from_int(s: int) -> str:
    if s == car.Status.VALID.value:
        return S_VALID
    elif s == car.Status.IN_RENT.value:
        return S_IN_RENT
    elif s == car.Status.PENDDING.value:
        return S_PENDDING
    elif s == car.Status.INVALID.value:
        return S_INVALID
    else:
        return None

class Car:
    car_id: int
    user_id: int
    make: str
    model: str
    year: int
    mileage: int
    rent_status: int
    min_rent_period: int
    max_rent_period: int
    limit: int

    def __init__(self):
        pass

    def search_with_conditions(self) -> (Response | list[dict]):
        '''
        Search cars with customized conditions
        '''

        op = car.CarTable()
        try:
            all = op.search_with_coditions(self.__dict__, self.limit)
            return all if all else []
        except Exception as e:
            return error_to_response(ServErrorCode.CommonError)


    def search_by_id(self, car_id: int) -> Response:
        '''
        Search a car's info
        '''

        if not car_id or car_id < 0:
            return error_to_response(ServErrorCode.CarInfoMissed, "Missed necessary info while searching a car.")

        op = car.CarTable()
        try:
            this_car = op.search(car_id)
            if not this_car:
                return error_to_response(ServErrorCode.CarRegisterFailed, 'Not find the registered car.')
            
            self.car_id = car_id
            self.user_id = this_car[car.Columns.USER_ID.value]
            self.make = this_car[car.Columns.MAKE.value]
            self.model = this_car[car.Columns.MODEL.value]
            self.year = this_car[car.Columns.YEAR.value]
            self.mileage = this_car[car.Columns.MILEAGE.value]
            self.rent_status = this_car[car.Columns.STATUS.value]
            self.min_rent_period = this_car[car.Columns.MIN_RENT_PERIOD.value]
            self.max_rent_period = this_car[car.Columns.MAX_RENT_PERIOD.value]
            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            return error_to_response(ServErrorCode.CommonError)

    def search_for_user(self, user_id: int, limit:int) -> (Response | list[dict]):
        if not user_id or user_id < 0:
            return error_to_response(ServErrorCode.CarInfoMissed, 'Invalid user id')

        op = car.CarTable()
        self.user_id = user_id
        try:
            all = op.search_for_users(self.user_id, order=f"ORDER BY {car.Columns.REGISTER.value} DESC {"LIMIT " + limit if not limit and limit > 0 else ""}")
            return all
        except Exception as e:
            return error_to_response(ServErrorCode.CommonError)

    def register(self) -> Response:
        '''
        Register a car, need to check user is admin
        '''

        Logger().debug(f'[model] register >> register a car: {self.__dict__}')

        if not self.user_id or not self.make or not self.model or not self.year or not self.mileage \
              or self.mileage <= 0 or self.min_rent_period <= 0 or self.max_rent_period < 0 :
            Logger().debug(f'[model] error >> info check failed while performing check. CarInfoMissed...')
            return error_to_response(ServErrorCode.CarInfoMissed, "Missed necessary info while registering a car.")

        op = car.CarTable()
        try:
            success = op.register({
                car.Columns.MAKE.value: self.make,
                car.Columns.USER_ID.value: self.user_id,
                car.Columns.MODEL.value: self.model,
                car.Columns.YEAR.value: self.year,
                car.Columns.MILEAGE.value: self.mileage,
                car.Columns.STATUS.value: self.rent_status,
                car.Columns.MIN_RENT_PERIOD.value: self.min_rent_period,
                car.Columns.MAX_RENT_PERIOD.value: self.max_rent_period
            })

            if not success:
                Logger().debug(f'[model] error >> car table perform failed. CarRegisterFailed...')
                return error_to_response(ServErrorCode.CarRegisterFailed)

            Logger().debug(f'[model] success >> car table perform success...')
            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            Logger().debug(f'[model] error >> car table perform exception: {e.__dict__}...')
            return error_to_response(ServErrorCode.CarRegisterFailed)

        

        

'''
Car model definition
@author shuohui liu
@date 10 Sep 2026
'''

from db import table_car as car
from exception import ServErrorCode
from lib import Response, exception_to_http_response

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
    if s == car.Status.VALID:
        return S_VALID
    elif s == car.Status.IN_RENT:
        return S_IN_RENT
    elif s == car.Status.PENDDING:
        return S_PENDDING
    elif s == car.Status.INVALID:
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
            return exception_to_http_response(e)


    def search_by_id(self, car_id: int) -> Response:
        '''
        Search a car's info
        '''

        if not car_id or car_id < 0:
            return Response(ServErrorCode.CarInfoMissed, "Missed necessary info while searching a car.")

        op = car.CarTable()
        try:
            this_car = op.search(car_id)
            if not this_car:
                return Response(ServErrorCode.CarRegisterFailed, 'Not find the registered car.')
            
            self.car_id = car_id
            self.user_id = this_car[car.Columns.USER_ID]
            self.make = this_car[car.Columns.MAKE]
            self.model = this_car[car.Columns.MODEL]
            self.year = this_car[car.Columns.YEAR]
            self.mileage = this_car[car.Columns.MILEAGE]
            self.rent_status = this_car[car.Columns.STATUS]
            self.min_rent_period = this_car[car.Columns.MIN_RENT_PERIOD]
            self.max_rent_period = this_car[car.Columns.MAX_RENT_PERIOD]
            return Response(ServErrorCode.Success)
        except Exception as e:
            return exception_to_http_response(e)

    def search_for_user(self, user_id: int, limit:int) -> (Response | list[dict]):
        if not user_id or user_id < 0:
            return Response(ServErrorCode.CarInfoMissed, 'Invalid user id')

        op = car.CarTable()
        self.user_id = user_id
        try:
            all = op.search_for_users(self.user_id, order=f"ORDER BY {car.Columns.REGISTER} DESC {"LIMIT " + limit if not limit and limit > 0 else ""}")
            return all
        except Exception as e:
            return exception_to_http_response(e)

    def register(self) -> Response:
        '''
        Register a car, need to check user is admin
        '''

        if not self.user_id or not self.make or not self.model or not self.year or not self.mileage \
              or self.mileage <= 0 or not self.rent_status \
              or not self.min_rent_period or self.min_rent_period <= 0 \
              or not self.max_rent_period or self.max_rent_period < 0 or \
                (self.max_rent_period > 0 and self.min_rent_period > self.max_rent_period):
            return Response(ServErrorCode.CarInfoMissed, "Missed necessary info while registering a car.")

        op = car.CarTable()
        try:
            success = op.register({
                car.Columns.MAKE: self.make,
                car.Columns.USER_ID: self.user_id,
                car.Columns.MODEL: self.model,
                car.Columns.YEAR: self.year,
                car.Columns.MILEAGE: self.mileage,
                car.Columns.STATUS: self.rent_status,
                car.Columns.MIN_RENT_PERIOD: self.min_rent_period,
                car.Columns.MAX_RENT_PERIOD: self.max_rent_period
            })

            if not success:
                return Response(ServErrorCode.CarRegisterFailed)

            return Response(ServErrorCode.Success)
        except Exception as e:
            return exception_to_http_response(e)

        

        

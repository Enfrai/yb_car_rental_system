'''
Booking model definition
@author shuohui liu
@date 11 Sep 2026
'''

from db import table_booking as bt
from exception import ServErrorCode
from lib import Response, exception_to_http_response, gen_unique_id

# S_RESERVED = 'reserved'     # 0
S_PENDDING = 'pendding'     # 1
S_APPROVED = 'approved'     # 2
S_REJECTED = 'rejected'     # 3
S_COMPLETED = 'completed'   # 4
S_CANCELLED = 'cancelled'   # 5

def booking_status_from_str(s: str) -> int:
    if S_PENDDING == s:
        return bt.Status.PENDDING.value
    elif S_APPROVED == s:
        return bt.Status.APPROVED.value
    elif S_REJECTED == s:
        return bt.Status.REJECTED.value
    elif S_COMPLETED == s: 
        return bt.Status.COMPLETED.value
    elif S_CANCELLED == s: 
        return bt.Status.CANCELLED.value
    else: 
        return None
    

def booking_status_from_int(s: int) -> str:
    if s == bt.Status.PENDDING:
        return S_PENDDING
    elif s == bt.Status.APPROVED:
        return S_APPROVED
    elif s == bt.Status.REJECTED:
        return S_REJECTED
    elif s == bt.Status.COMPLETED:
        return S_COMPLETED
    elif s == bt.Status.CANCELLED:
        return S_CANCELLED
    else:
        return None

class Book:
    book_id: int
    book_uid: int
    customer_id: int
    admin_id: int
    car_id: int
    start_date: str
    end_date: str
    total_fee: int
    status: int
    create_time: str
    limit: int

    def __init__(self):
        pass

    # =================================================================
    def book_a_car(self) -> Response:
        '''
        Book a car
        '''

        if not self.customer_id or not self.admin_id or not self.car_id \
              or not self.start_date <= 0 or not self.end_date \
              or (not self.total_fee and self.total_fee > 0) or not self.status:
            return Response(ServErrorCode.CarInfoMissed, "Missed necessary info while registering a car.")

        op = bt.OrderTable
        try:
            book_uid = gen_unique_id()
            success = op.book({
                bt.Columns.UID: self.book_uid,
                bt.Columns.CUSTOMER_ID: self.customer_id,
                bt.Columns.ADMIN_ID: self.admin_id,
                bt.Columns.CAR_ID: self.car_id,
                bt.Columns.START_DATE: self.start_date,
                bt.Columns.END_DATE: self.end_date,
                bt.Columns.TOTAL_FEE: self.total_fee,
                bt.Columns.STATUS: self.status,
            })

            if not success:
                return Response(ServErrorCode.CarRegisterFailed)

            self.book_uid = book_uid
            return Response(ServErrorCode.Success)
        except Exception as e:
            return exception_to_http_response(e)

    # =================================================================
    def search_with_conditions(self) -> (Response | list[dict]):
        '''
        Search order with customized conditions
        '''

        op = bt.OrderTable()
        try:
            all = op.search(self.customer_id, self.admin_id, self.book_id, self.status, 
                            extras=self.__dict__, 
                            limit=self.limit)
            return all if all else []
        except Exception as e:
            return exception_to_http_response(e)

    #===========================


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

        

'''
Booking model definition
@author shuohui liu
@date 11 Sep 2026
'''

from db import table_booking as bt
from exception import ServErrorCode
from lib import Response, gen_unique_id, SortOrder, error_to_response, Logger

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
    if s == bt.Status.PENDDING.value:
        return S_PENDDING
    elif s == bt.Status.APPROVED.value:
        return S_APPROVED
    elif s == bt.Status.REJECTED.value:
        return S_REJECTED
    elif s == bt.Status.COMPLETED.value:
        return S_COMPLETED
    elif s == bt.Status.CANCELLED.value:
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
    where: str

    def __init__(self):
        pass

    # =================================================================
    def book_a_car(self) -> Response:
        '''
        Book a car
        '''

        Logger().debug(f'[model] book_a_car >> Booking a car {self.__dict__}')

        if not self.customer_id or not self.admin_id or not self.car_id \
              or not self.start_date <= 0 or not self.end_date \
              or (not self.total_fee and self.total_fee > 0) or not self.status:
            Logger().debug(f'[model] error >> missed info while checking...')
            return error_to_response(ServErrorCode.CarInfoMissed, "Missed necessary info while registering a car.")

        op = bt.OrderTable
        try:
            book_uid = gen_unique_id()
            success = op.book({
                bt.Columns.UID.value: self.book_uid,
                bt.Columns.CUSTOMER_ID.value: self.customer_id,
                bt.Columns.ADMIN_ID.value: self.admin_id,
                bt.Columns.CAR_ID.value: self.car_id,
                bt.Columns.START_DATE.value: self.start_date,
                bt.Columns.END_DATE.value: self.end_date,
                bt.Columns.TOTAL_FEE.value: self.total_fee,
                bt.Columns.STATUS.value: self.status,
            })

            if not success:
                Logger().debug(f'[model] error >> order table exec error, OrderGenFailed...')
                return error_to_response(ServErrorCode.OrderGenFailed)

            self.book_uid = book_uid
            Logger().debug(f'[model] success >> order gen: bookid: {book_uid}...')
            return error_to_response(ServErrorCode.Success)
        except Exception as e:
            Logger().debug(f'[model] error >> order table exec exception, {e}...')
            return error_to_response(ServErrorCode.OrderGenFailed)

    # =================================================================
    def search_with_conditions(self, create_order: SortOrder) -> (Response | list[dict]):
        '''
        Search order with customized conditions
        '''

        op = bt.OrderTable()
        try:
            order_by = None
            if SortOrder.DESC == create_order:
                order_by = f" ORDER BY {bt.Columns.CREATE_TIME.value} DESC"
            elif SortOrder.ASC == create_order:
                order_by = f" ORDER BY {bt.Columns.CREATE_TIME.value} ASC"

            all = op.search(self.customer_id, self.admin_id, self.book_id, self.status, 
                            where=self.where,
                            extras=self.__dict__, 
                            limit=self.limit,
                            order_by=order_by)
            return all if all else []
        except Exception as e:
            return error_to_response(ServErrorCode.CommonError)

    
    # =================================================================
    def search_by_status(self, *args, create_order: SortOrder = None) -> (Response | list[dict]):
        '''
        Search order with customized conditions
        '''

        op = bt.OrderTable()
        try:
            order_by = None
            if SortOrder.DESC == create_order:
                order_by = f" ORDER BY {bt.Columns.CREATE_TIME.value} DESC"
            elif SortOrder.ASC == create_order:
                order_by = f" ORDER BY {bt.Columns.CREATE_TIME.value} ASC"

            where = None
            where_values = ()
            if len(args) > 0:
                where = f' WHERE {bt.Columns.STATUS.value} in ({", ".join(["?"] * len(args))})'
                for e in args:
                    if isinstance(e, bt.Status):
                        where_values += (e.value,)
                    elif isinstance(e, int):
                        where_values += (e,)

            all = op.search_where_clause(self.customer_id, self.admin_id, order_by=order_by,
                            where=where, 
                            where_values=where_values, 
                            extras=None)
            return all if all else []
        except Exception as e:
            return error_to_response(ServErrorCode.CommonError)

    #===========================
    def where_status_in(self, *args) -> str:
        if not args:
            return ''

        return f'WHERE {bt.Columns.STATUS.value} in ({", ".join(['?'] * len(args))})'

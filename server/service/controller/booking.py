from pydantic import BaseModel, Field
from lib import Response, HTTPResponse, exception_to_http_response, error_to_response, error_to_http_response
from service import model, view, controller
from exception import ServErrorCode
from db import table_booking as bt, table_car as ct, table_user as ut
import random

class BookingCarRequest(BaseModel):
    customer_id: str = Field(...)
    admin_id: str = Field(...)
    car_id: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)
    total_fee: int = Field(...)
    status: str = Field(...)
    create_time: str = Field(...)
    
class BookingHistoryRequest(BaseModel):
    customer_id: str = Field(...)
    admin_id: str = Field(...)

class BookingConfirmRequest(BaseModel):
    order_id: str = Field(...)
    user_id: str = Field(...)
    status: str = Field(...)


class BookingController:
    def __init__(self):
        pass

    def confirm_order(self, req: BookingConfirmRequest) -> HTTPResponse:
        '''
        Confirm an order'''

        if not req.order_id:
            return error_to_http_response(ServErrorCode.OrderInfoMissed, 'Missing necessary order id.')

        status = model.booking_status_from_str(status)
        if not status:
            return error_to_http_response(ServErrorCode.OrderInfoMissed, 'Wrong status.')
        
        op = bt.OrderTable()
        success = op.update(req.order_id, {
            bt.Columns.STATUS.value: status,
            bt.Columns.ADMIN_ID.value: req.user_id,
        })

        if not success:
            return error_to_http_response(ServErrorCode.OrderConfirmError, 'Confirm failed.')

        return error_to_http_response(ServErrorCode.Success)

    def search_orders_by_user(self, req: BookingHistoryRequest) -> HTTPResponse:
        '''
        search orders by user (customer or admin)
        '''

        if not req.admin_id and not req.customer_id:
            return error_to_http_response(ServErrorCode.OrderSearchError, 'Missing specific user.')

        op = model.Book()
        op.customer_id = req.customer_id
        op.admin_id = req.admin_id
        resp = op.search_with_conditions()
        if isinstance(resp, Response):
            return HTTPResponse(resp.code, resp.message, resp.detail)
        elif not isinstance(resp, list):
            return error_to_http_response(ServErrorCode.CommonError)

        all = []
        for info in resp:
            book_id = info.get(bt.Columns.ID.value, None)
            customer_id = info.get(bt.Columns.CUSTOMER_ID.value, None)
            admin_id = info.get(bt.Columns.ADMIN_ID.value, None)
            car_id = info.get(bt.Columns.CAR_ID.value, None)
            start_date = info.get(bt.Columns.START_DATE.value, None)
            end_date = info.get(bt.Columns.END_DATE.value, None)
            total_fee = info.get(bt.Columns.TOTAL_FEE.value, None)
            status = info.get(bt.Columns.STATUS.value, None)
            create_time = info.get(bt.Columns.CREATE_TIME.value, None)

            data = view.BookInfoData().build(
                book_id, customer_id, admin_id, car_id,
                start_date, end_date, total_fee, 
                model.booking_status_from_int(status) if status else None, 
                create_time
            )
            all.append(data)

        return error_to_http_response(ServErrorCode.Success)
            

    def book_a_car(self, req: BookingCarRequest) -> HTTPResponse:
        '''
        Book a car
        '''

        # search all booked cars for user
        booker = model.Book()
        booker.customer_id = int(req.customer_id) if req.customer_id else None
        resp = booker.search_by_status(bt.Status.RESERVED, bt.Status.COMPLETED, bt.Status.CANCELLED, bt.Status.REJECTED, create_order=None)
        if isinstance(resp, Response):
            return HTTPResponse(resp.code, resp.message, resp.detail)
        elif not isinstance(resp, list):
            return error_to_http_response(ServErrorCode.CommonError)

        can_book = len(resp) > 0
        if not can_book:
            return error_to_http_response(ServErrorCode.OrderGenFailed, 'Having in-process orders')

        # book action
        booker = model.Book()
        booker.customer_id = int(req.customer_id) if req.customer_id else None
        booker.admin_id = int(req.admin_id) if req.admin_id else None
        booker.car_id = int(req.car_id) if req.car_id else None
        booker.start_date = req.start_date
        booker.end_date = req.end_date
        booker.total_fee = req.total_fee
        booker.status = model.booking_status_from_str(req.status)

        # make a admin_id to this order
        if not booker.admin_id:
            op = ut.UserTable()
            users = op.search_all_users(is_admin=True)
            if len(users) == 0:
                return error_to_http_response(ServErrorCode.UserNoAdminExist)
            
            seed = random.randrange(0, len(users))
            user = users[seed]
            booker.admin_id = user.get(ut.Columns.ID.value)

        # continue to book process
        resp = booker.book_a_car()
        if not resp.is_success():
            return error_to_http_response(ServErrorCode.OrderGenFailed)

        # search order info
        book_uid = booker.book_uid
        booker = model.Book()
        booker.book_uid = book_uid
        booker.limit = 1
        resp = booker.search_with_conditions()
        if isinstance(resp, Response):
            return HTTPResponse(resp.code, resp.message, resp.detail)
        elif isinstance(resp, list) and len(resp) == 1:
            info = resp[0]
            book_id = info.get(bt.Columns.ID.value, None)
            customer_id = info.get(bt.Columns.CUSTOMER_ID.value, None)
            admin_id = info.get(bt.Columns.ADMIN_ID.value, None)
            car_id = info.get(bt.Columns.CAR_ID.value, None)
            start_date = info.get(bt.Columns.START_DATE.value, None)
            end_date = info.get(bt.Columns.END_DATE.value, None)
            total_fee = info.get(bt.Columns.TOTAL_FEE.value, None)
            status = info.get(bt.Columns.STATUS.value, None)
            create_time = info.get(bt.Columns.CREATE_TIME.value, None)

            # sync car status to car table
            car = ct.CarTable()
            try:
                success = car.update(car_id, {
                    ct.Columns.STATUS.value: ct.Status.PENDDING.value,
                })

                if not success:
                    return error_to_http_response(ServErrorCode.CommonError, 'Error while sync PENDDING status to car table.')
            except Exception as e:
                return error_to_http_response(ServErrorCode.CommonError, f'{e}')

            # continue to response to client
            data = view.BookInfoData().build(
                book_id, customer_id, admin_id, car_id,
                start_date, end_date, total_fee, 
                model.booking_status_from_int(status) if status else None, 
                create_time
            )
            return error_to_http_response(ServErrorCode.Success)
        else:
            return error_to_http_response(ServErrorCode.OrderGenFailed)
from pydantic import BaseModel, Field
from lib import Response, HTTPResponse, exception_to_http_response
from service import model, view, controller
from exception import ServErrorCode
from db import table_booking as bt


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

class BookingController:
    def __init__(self):
        pass

    def search_orders_by_user(self, req: BookingHistoryRequest) -> HTTPResponse:
        '''
        search orders by user (customer or admin)
        '''

        if not req.admin_id and not req.customer_id:
            r = Response(ServErrorCode.OrderSearchError, 'Missing specific user.')
            return HTTPResponse(r.code, r.message, r.detail)

        op = model.Book()
        op.customer_id = req.customer_id
        op.admin_id = req.admin_id
        resp = op.search_with_conditions()
        if isinstance(resp, Response):
            return HTTPResponse(resp.code, resp.message, resp.detail)
        elif not isinstance(resp, list):
            r = Response(ServErrorCode.CommonError)
            return HTTPResponse(r.code, r.message, r.detail)

        all = []
        for info in resp:
            book_id = info.get(bt.Columns.ID, None)
            customer_id = info.get(bt.Columns.CUSTOMER_ID, None)
            admin_id = info.get(bt.Columns.ADMIN_ID, None)
            car_id = info.get(bt.Columns.CAR_ID, None)
            start_date = info.get(bt.Columns.START_DATE, None)
            end_date = info.get(bt.Columns.END_DATE, None)
            total_fee = info.get(bt.Columns.TOTAL_FEE, None)
            status = info.get(bt.Columns.STATUS, None)
            create_time = info.get(bt.Columns.CREATE_TIME, None)

            data = view.BookInfoData().build(
                book_id, customer_id, admin_id, car_id,
                start_date, end_date, total_fee, 
                model.booking_status_from_int(status) if status else None, 
                create_time
            )
            all.append(data)

        r = Response(ServErrorCode.Success)
        return HTTPResponse(r.code, r.message, r.detail, data)
            

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
            r = Response(ServErrorCode.CommonError)
            return HTTPResponse(r.code, r.message, r.detail)

        can_book = len(resp) > 0
        if not can_book:
            r = Response(ServErrorCode.OrderGenFailed, 'Having in-process orders')
            return HTTPResponse(r.code, r.message, r.detail)

        # book action
        booker = model.Book()
        booker.customer_id = int(req.customer_id) if req.customer_id else None
        booker.admin_id = int(req.admin_id) if req.admin_id else None
        booker.car_id = int(req.car_id) if req.car_id else None
        booker.start_date = req.start_date
        booker.end_date = req.end_date
        booker.total_fee = req.total_fee
        booker.status = model.booking_status_from_str(req.status)

        resp = booker.book_a_car()
        if not resp.is_success():
            r = Response(ServErrorCode.OrderGenFailed)
            return HTTPResponse(r.code, r.message, r.detail)

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
            book_id = info.get(bt.Columns.ID, None)
            customer_id = info.get(bt.Columns.CUSTOMER_ID, None)
            admin_id = info.get(bt.Columns.ADMIN_ID, None)
            car_id = info.get(bt.Columns.CAR_ID, None)
            start_date = info.get(bt.Columns.START_DATE, None)
            end_date = info.get(bt.Columns.END_DATE, None)
            total_fee = info.get(bt.Columns.TOTAL_FEE, None)
            status = info.get(bt.Columns.STATUS, None)
            create_time = info.get(bt.Columns.CREATE_TIME, None)

            data = view.BookInfoData().build(
                book_id, customer_id, admin_id, car_id,
                start_date, end_date, total_fee, 
                model.booking_status_from_int(status) if status else None, 
                create_time
            )
            r = Response(ServErrorCode.Success)
            return HTTPResponse(r.code, r.message, r.detail, data)
        else:
            r = Response(ServErrorCode.OrderGenFailed)
            return HTTPResponse(r.code, r.message, r.detail)
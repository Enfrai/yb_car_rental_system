from lib import Data
from lib import safe_string

class BookIdData(Data):
    book_id: str

    def __init__(self, book_id, *args, **kwargs):
        super().__init__(
            book_id = f'{book_id}' if book_id else book_id if isinstance(book_id, str) else ''
        )


class BookInfoData(Data):
    book_id: str
    customer_id: str
    admin_id: str
    car_id: str
    start_date: str
    end_date: str
    total_fee: int
    status: str
    create_time: str
    
    def __init__(self, book_id, # int
                customer_id, # int
                admin_id, # int
                car_id, # int
                start_date: str,
                end_date: str,
                total_fee: int,
                status: str,
                create_time: str,
                *args, **kwargs
        ):

        super().__init__(
            book_id = f'{book_id}' if book_id else book_id if isinstance(book_id, str) else '',
            customer_id = f'{customer_id}' if customer_id else customer_id if isinstance(customer_id, str) else '',
            admin_id = f'{admin_id}' if admin_id else admin_id if isinstance(admin_id, str) else '',
            car_id = f'{car_id}' if car_id else car_id if isinstance(car_id, str) else '',
            start_date = start_date,
            end_date = end_date,
            total_fee = total_fee,
            status = status,
            *args, **kwargs
        )


class BookInfoList(Data):
    orders: list[BookInfoData] = []

    def __init__(self, data: list[BookInfoData], *args, **kwargs):
        super().__init__(data=data, *args, **kwargs)
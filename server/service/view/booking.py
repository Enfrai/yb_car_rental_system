from lib import Data
from lib import safe_string

class BookIdData(Data):
    book_id: str

    def __init__(self, book_id: int):
        self.car_id = f'{book_id}' if book_id else ''

    def to_dict(self) -> dict:
        return self.__dict__

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
    
    def build(self, book_id: int,
                customer_id: int,
                admin_id: int,
                car_id: int,
                start_date: str,
                end_date: str,
                total_fee: int,
                status: str
        ):
        self.car_id = f'{car_id}' if car_id else ''
        self.book_id = f'{book_id}' if book_id else ''
        self.customer_id = f'{customer_id}' if customer_id else ''
        self.admin_id = f'{admin_id}' if admin_id else ''
        self.start_date = start_date
        self.end_date = end_date
        self.total_fee = total_fee
        self.status = status

        return self

    def to_dict(self) -> dict:
        return self.__dict__

class BookInfoList(Data):
    orders: list[BookInfoData] = []

    def build(self, data: list[BookInfoData] = []):
        self.cars = data
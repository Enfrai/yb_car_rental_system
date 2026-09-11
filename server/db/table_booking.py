'''
Definition and implementation for car table.
@author shuohui liu
@date 10 Sep 2026
'''

from enum import Enum
from .db_helper import db_helper
from exception.db_error import DBExeError, ServErrorCode
from exception.booking_error import OrderError

class Status(Enum):
    RESERVED = 0
    PENDDING = 1
    APPROVED = 2
    REJECTED = 3
    COMPLETED = 4
    CANCELLED = 5

_TABLE_NAME = "booking"

class Columns(Enum):
    ID = "book_id"
    CUSTOMER_ID = "customer_id"
    ADMIN_ID = "admin_id"
    CAR_ID = "car_id"
    START_DATE = "start_date"
    END_DATE = "end_date"
    TOTAL_FEE = "total_fee"
    STATUS = "status"
    CREATE_TIME = "create_time"

class OrderTable:
    def __init__(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
                {Columns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Columns.CUSTOMER_ID} INTEGER NOT NULL,
                {Columns.ADMIN_ID} INTEGER,
                {Columns.CAR_ID} INTEGER NOT NULL,
                {Columns.START_DATE} DATETIME NOT NULL,
                {Columns.END_DATE} DATETIME NOT NULL,
                {Columns.TOTAL_FEE} INTEGER NOT NULL,
                {Columns.STATUS} INTEGER DEFAULT {Status.PENDDING.value},
                {Columns.CREATE_TIME} DATETIME DEFAULT (datetime("now", "localtime"))
            )
        '''
        db_helper.execute_non_query(sql)

    def update(self, book_id: int, info: dict) -> bool:
        '''
        update specific booking info
        '''

        columns = []
        values = ()

        if info is None or book_id is None:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'Order info is missed while booking a car.')
        
        admin_id = info.get(Columns.ADMIN_ID, None)
        if admin_id is not None:
            columns.append(f'{Columns.ADMIN_ID}=?')
            values += (admin_id,)

        status = info.get(Columns.STATUS, None)
        if status is not None:
            columns.append(f'{Columns.STATUS}=?')
            values += (status,)

        car_id = info.get(Columns.CAR_ID, None)
        if car_id is not None:
            columns.append(f'{Columns.CAR_ID}=?')
            values += (car_id,)

        start_date = info.get(Columns.START_DATE, None)
        if start_date is not None:
            columns.append(f'{Columns.START_DATE}=?')
            values += (start_date,)

        end_date = info.get(Columns.END_DATE, None)
        if end_date is not None:
            columns.append(f'{Columns.END_DATE}=?')
            values += (end_date,)

        total_fee = info.get(Columns.TOTAL_FEE, None)
        if total_fee is not None:
            columns.append(f'{Columns.TOTAL_FEE}=?')
            values += (total_fee,)

        if len(columns) == 0:
            return True

        values += (book_id,)
        sql = f'''
            UPDATE {_TABLE_NAME}
            SET {", ".join(columns)}
            WHERE {Columns.ID} =?
        '''
        ret = db_helper.execute_non_query(sql, values)
        return ret == 0


    def book(self, info: dict) -> bool: 
        '''
        Register and add on booking record.
        '''

        columns = []
        values = ()

        if info is None:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'Order info is missed while booking a car.')
        
        customer_id = info.get(Columns.CUSTOMER_ID, None)
        if customer_id is not None:
            columns.append(f'{Columns.CUSTOMER_ID}')
            values += (customer_id,)
        
        admin_id = info.get(Columns.ADMIN_ID, None)
        if admin_id is not None:
            columns.append(f'{Columns.ADMIN_ID}')
            values += (admin_id,)

        status = info.get(Columns.STATUS, None)
        if status is not None:
            columns.append(f'{Columns.STATUS}')
            values += (status,)

        car_id = info.get(Columns.CAR_ID, None)
        if car_id is not None:
            columns.append(f'{Columns.CAR_ID}')
            values += (car_id,)

        start_date = info.get(Columns.START_DATE, None)
        if start_date is not None:
            columns.append(f'{Columns.START_DATE}')
            values += (start_date,)

        end_date = info.get(Columns.END_DATE, None)
        if end_date is not None:
            columns.append(f'{Columns.END_DATE}')
            values += (end_date,)

        total_fee = info.get(Columns.TOTAL_FEE, None)
        if total_fee is not None:
            columns.append(f'{Columns.TOTAL_FEE}')
            values += (total_fee,)

        if len(columns) == 0:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'No info provided while generating an order.')

        if customer_id is None or car_id is None or start_date is None or end_date is None or total_fee is None:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'Necessary info is missed while generating an order.')

        sql = f'''
            INSERT INTO {_TABLE_NAME} 
            ({", ".join(columns)})
            VALUES 
            ({", ".join(["?" * len(columns)])})
        '''
        ret = db_helper.execute_non_query(sql, values)
        return ret == 0

    def search(self, customer_id:int, admin_id:int, order_id:int, order_status:int) -> list:
        '''
        To look up a customer's orders.
        '''

        condition = []
        values = ()
        if customer_id is not None:
            condition.append(Columns.CUSTOMER_ID + " = ?")
            values += (customer_id,)

        if admin_id is not None:
            condition.append(Columns.ADMIN_ID + " = ?")
            values += (admin_id,)

        if order_id is not None:
            condition.append(Columns.ID + " = ?")
            values += (order_id,)

        if order_status is not None:
            condition.append(Columns.STATUS + " = ?")
            values += (order_status,)

        if len(condition) == 0: 
            raise OrderError(ServErrorCode.OrderInfoMissed, "Must provide necessary conditions while invoking search() from OrderTable.")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {" AND ".join(condition)}
        '''
        list = db_helper.execute_query(sql, values)
        ret = []
        for row in list:
            ret.append(dict(row))
        return ret
        
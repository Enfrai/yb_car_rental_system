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
    UID = "u_book_id"
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
                {Columns.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Columns.UID.value} INTEGER NOT NULL,
                {Columns.CUSTOMER_ID.value} INTEGER NOT NULL,
                {Columns.ADMIN_ID.value} INTEGER,
                {Columns.CAR_ID.value} INTEGER NOT NULL,
                {Columns.START_DATE.value} DATETIME NOT NULL,
                {Columns.END_DATE.value} DATETIME NOT NULL,
                {Columns.TOTAL_FEE.value} INTEGER NOT NULL,
                {Columns.STATUS.value} INTEGER DEFAULT {Status.PENDDING.value},
                {Columns.CREATE_TIME.value} DATETIME DEFAULT (datetime("now", "localtime"))
            )
        '''
        db_helper.execute_non_query(sql)
        db_helper.commit()

    def _row_to_dict(self, row) -> dict:
        return {
            Columns.ID.value: row[0],
            Columns.UID.value: row[1],
            Columns.CUSTOMER_ID.value: row[2],
            Columns.ADMIN_ID.value: row[3],
            Columns.CAR_ID.value: row[4],
            Columns.START_DATE.value: row[5],
            Columns.END_DATE.value: row[6],
            Columns.TOTAL_FEE.value: row[7],
            Columns.STATUS.value: row[8],
            Columns.CREATE_TIME.value: row[9],
        }

    def update(self, book_id: int, info: dict) -> bool:
        '''
        update specific booking info
        '''

        columns = []
        values = ()

        if not info or not book_id:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'Order info is missed while booking a car.')
        
        admin_id = info.get(Columns.ADMIN_ID.value, None)
        if not admin_id:
            columns.append(f'{Columns.ADMIN_ID.value}=?')
            values += (admin_id,)

        status = info.get(Columns.STATUS.value, None)
        if status is not None:
            columns.append(f'{Columns.STATUS.value}=?')
            values += (status,)

        car_id = info.get(Columns.CAR_ID.value, None)
        if not car_id:
            columns.append(f'{Columns.CAR_ID.value}=?')
            values += (car_id,)

        start_date = info.get(Columns.START_DATE.value, None)
        if not start_date:
            columns.append(f'{Columns.START_DATE.value}=?')
            values += (start_date,)

        end_date = info.get(Columns.END_DATE.value, None)
        if not end_date:
            columns.append(f'{Columns.END_DATE.value}=?')
            values += (end_date,)

        total_fee = info.get(Columns.TOTAL_FEE.value, None)
        if not total_fee:
            columns.append(f'{Columns.TOTAL_FEE.value}=?')
            values += (total_fee,)

        if len(columns) == 0:
            return True

        values += (book_id,)
        sql = f'''
            UPDATE {_TABLE_NAME}
            SET {", ".join(columns)}
            WHERE {Columns.ID.value} =?
        '''
        ret = db_helper.execute_non_query(sql, values)
        if ret == 0:
            # True
            db_helper.commit()
            return True
        else:
            db_helper.rollback()
            return False


    def book(self, info: dict) -> bool: 
        '''
        Register and add on booking record.
        '''

        columns = []
        values = ()

        if not info:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'Order info is missed while booking a car.')
        
        uid = info.get(Columns.UID.value, None)
        if not uid:
            columns.append(f'{Columns.UID.value}')
            values += (uid,)
        
        customer_id = info.get(Columns.CUSTOMER_ID.value, None)
        if not customer_id:
            columns.append(f'{Columns.CUSTOMER_ID.value}')
            values += (customer_id,)
        
        admin_id = info.get(Columns.ADMIN_ID.value, None)
        if not admin_id:
            columns.append(f'{Columns.ADMIN_ID.value}')
            values += (admin_id,)

        status = info.get(Columns.STATUS.value, None)
        if status is not None:
            columns.append(f'{Columns.STATUS.value}')
            values += (status,)

        car_id = info.get(Columns.CAR_ID.value, None)
        if not car_id:
            columns.append(f'{Columns.CAR_ID.value}')
            values += (car_id,)

        start_date = info.get(Columns.START_DATE.value, None)
        if not start_date:
            columns.append(f'{Columns.START_DATE.value}')
            values += (start_date,)

        end_date = info.get(Columns.END_DATE.value, None)
        if not end_date:
            columns.append(f'{Columns.END_DATE.value}')
            values += (end_date,)

        total_fee = info.get(Columns.TOTAL_FEE.value, None)
        if not total_fee:
            columns.append(f'{Columns.TOTAL_FEE.value}')
            values += (total_fee,)

        if len(columns) == 0:
            raise OrderError(ServErrorCode.OrderInfoMissed, 'No info provided while generating an order.')

        sql = f'''
            INSERT INTO {_TABLE_NAME} 
            ({", ".join(columns)})
            VALUES 
            ({", ".join(["?" * len(columns)])})
        '''
        ret = db_helper.execute_non_query(sql, values)
        if ret == 0:
            # True
            db_helper.commit()
            return True
        else:
            db_helper.rollback()
            return False

    def search(self, customer_id:int, admin_id:int, order_id:int, order_status:int,
               extras:dict = None, limit:int = None, order_by: str = None) -> list[dict]:
        '''
        To look up a customer's orders.
        '''

        condition = []
        values = ()
        if customer_id is not None:
            condition.append(Columns.CUSTOMER_ID.value + " = ?")
            values += (customer_id,)

        if admin_id is not None:
            condition.append(Columns.ADMIN_ID.value + " = ?")
            values += (admin_id,)

        if order_id is not None:
            condition.append(Columns.ID.value + " = ?")
            values += (order_id,)

        if order_status is not None:
            condition.append(Columns.STATUS.value + " = ?")
            values += (order_status,)

        if extras:
            book_uid = extras.get(Columns.UID.value, None)
            if book_uid:
                condition.append(Columns.UID.value + " = ?")
                values += (book_uid,)

            car_id = extras.get(Columns.CAR_ID.value, None)
            if car_id:
                condition.append(Columns.CAR_ID.value + " = ?")
                values += (car_id,)

            start_date = extras.get(Columns.START_DATE.value, None)
            if start_date:
                condition.append(Columns.START_DATE.value + " = ?")
                values += (start_date,)

            end_date = extras.get(Columns.END_DATE.value, None)
            if end_date:
                condition.append(Columns.END_DATE.value + " = ?")
                values += (end_date,)

            create_date = extras.get(Columns.CREATE_TIME.value, None)
            if create_date:
                condition.append(Columns.CREATE_TIME.value + " = ?")
                values += (create_date,)

        sql = f'''
            SELECT * FROM {_TABLE_NAME} 
        '''

        if len(condition) > 0:
            sql += f' WHERE {" AND ".join(condition)} '

        if not order_by:
            sql += order_by

        list = db_helper.execute_query(sql, values)
        ret = []
        for row in list:
            ret.append(dict(row))
        return ret

    def search_where_clause(self, customer_id:int, admin_id:int, order_by: str = None, extras:dict = None, 
                            where: str = None, where_values: tuple = None) -> list[dict]:
        '''
        To look up a customer's orders.
        '''

        condition = []
        values = ()
        if customer_id is not None:
            condition.append(Columns.CUSTOMER_ID.value + " = ?")
            values += (customer_id,)

        if admin_id is not None:
            condition.append(Columns.ADMIN_ID.value + " = ?")
            values += (admin_id,)

        if extras:
            order_id = extras.get(Columns.ID.value, None)
            if order_id is not None:
                condition.append(Columns.ID.value + " = ?")
                values += (order_id,)

            order_status = extras.get(Columns.STATUS.value, None)
            if order_status is not None:
                condition.append(Columns.STATUS.value + " = ?")
                values += (order_status,)

            book_uid = extras.get(Columns.UID.value, None)
            if book_uid:
                condition.append(Columns.UID.value + " = ?")
                values += (book_uid,)

            car_id = extras.get(Columns.CAR_ID.value, None)
            if car_id:
                condition.append(Columns.CAR_ID.value + " = ?")
                values += (car_id,)

            start_date = extras.get(Columns.START_DATE.value, None)
            if start_date:
                condition.append(Columns.START_DATE.value + " = ?")
                values += (start_date,)

            end_date = extras.get(Columns.END_DATE.value, None)
            if end_date:
                condition.append(Columns.END_DATE.value + " = ?")
                values += (end_date,)

            create_date = extras.get(Columns.CREATE_TIME.value, None)
            if create_date:
                condition.append(Columns.CREATE_TIME.value + " = ?")
                values += (create_date,)

        sql = f'''
            SELECT * FROM {_TABLE_NAME} 
        '''

        where_clause = where
        if where_clause:
            sql += where_clause

        if len(condition) > 0:
            if where:
                where_clause += f' AND {" AND ".join(condition)} '
                sql += where_clause
            else:
                sql += f' WHERE {" AND ".join(condition)} '

        if not order_by:
            sql += order_by

        list = db_helper.execute_query(sql, values)
        ret = []
        for row in list:
            ret.append(dict(row))
        return ret
        
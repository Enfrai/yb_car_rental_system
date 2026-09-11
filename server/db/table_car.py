'''
Definition and implementation for car table.
@author shuohui liu
@date 10 Sep 2026
'''

from enum import Enum
from .db_helper import db_helper
from exception.db_error import DBExeError, ServErrorCode
from exception.car_error import CarError

class Columns(Enum):
    ID = "car_id"
    USER_ID = 'user_id'
    MAKE = "make"
    MODEL = "model"
    YEAR = "year"
    MILEAGE = "mileage"     # in meters
    REGISTER = "register_date"
    STATUS = "rent_status"
    MIN_RENT_PERIOD = "min_rent_period"
    MAX_RENT_PERIOD = "max_rent_period"

class Status(Enum):
    VALID = 0
    IN_RENT = 1
    PENDDING = 2
    INVALID = -1

_TABLE_NAME = "cars"

class CarTable:
    def __init__(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
                {Columns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Columns.USER_ID} INTEGER NOT NULL,
                {Columns.MAKE} CHAR(128) NOT NULL,
                {Columns.MODEL} CHAR(128) NOT NULL,
                {Columns.YEAR} INTEGER NOT NULL,
                {Columns.MILEAGE} INTEGER DEFAULT 0,
                {Columns.REGISTER} DATETIME DEFAULT (datetime("now", "localtime")),
                {Columns.STATUS} INTEGER DEFAULT {Status.VALID.value},
                {Columns.MIN_RENT_PERIOD} INTEGER DEFAULT 1,
                {Columns.MAX_RENT_PERIOD} INTEGER DEFAULT 0
            )
        '''
        db_helper.execute_non_query(sql)

    def update(self, car_id: int, car: dict) -> bool:
        '''
        update specific car info, normally for mileage, status, min_rent_period, max_rent_period
        '''

        columns = []
        values = ()

        if not car or not car_id:
            raise CarError(ServErrorCode.CarInfoMissed, 'Car info is missed while updating a car.')
        
        mileage = car.get(Columns.MILEAGE, None)
        if mileage is not None:
            columns.append(f'{Columns.MILEAGE}=?')
            values += (mileage,)

        status = car.get(Columns.STATUS, None)
        if status is not None:
            columns.append(f'{Columns.STATUS}=?')
            values += (status,)

        min_rent_period = car.get(Columns.MIN_RENT_PERIOD, None)
        if min_rent_period is not None:
            columns.append(f'{Columns.MIN_RENT_PERIOD}=?')
            values += (min_rent_period,)

        max_rent_period = car.get(Columns.MAX_RENT_PERIOD, None)
        if max_rent_period is not None:
            columns.append(f'{Columns.MAX_RENT_PERIOD}=?')
            values += (max_rent_period,)

        if len(columns) == 0:
            return True

        values += (car_id,)
        sql = f'''
            UPDATE {_TABLE_NAME}
            SET {", ".join(columns)}
            WHERE {Columns.ID} =?
        '''
        ret = db_helper.execute_non_query(sql, values)
        return ret == 0


    def register(self, car: dict) -> bool: 
        '''
        Register and add on car record.
        '''

        car_checked = False

        if car is not None:
            user_id = car.get(Columns.USER_ID, None)
            make = car.get(Columns.MAKE, None)
            model = car.get(Columns.MODEL, None)
            year = car.get(Columns.YEAR, None)
            mileage = car.get(Columns.MILEAGE, None)
            register = car.get(Columns.REGISTER, None)
            min_rent_period = car.get(Columns.MIN_RENT_PERIOD, 1)
            max_rent_period = car.get(Columns.MAX_RENT_PERIOD, 0)

            car_checked = not user_id and not make and not model and not year and not mileage and not register \
                and not min_rent_period and not max_rent_period

        if not car_checked:
            raise CarError(ServErrorCode, 'Car necessary info missed while registering a car.')

        sql = f'''
            INSERT INTO {_TABLE_NAME} 
            ({Columns.MAKE}, {Columns.MODEL}, {Columns.YEAR}, {Columns.MILEAGE}, {Columns.REGISTER}, {Columns.MIN_RENT_PERIOD}, {Columns.MAX_RENT_PERIOD})
            VALUES 
            (?, ?, ?, ?, ?, ?, ?)
        '''
        ret = db_helper.execute_non_query(sql, (make, model, year, mileage, register, min_rent_period, max_rent_period))
        return ret == 0


    def exist(self, car_id:int) -> bool:
        '''
        To check if one car is exist.
        '''

        if not car_id: 
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide car_id while invoking exist() from CarTable.")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.ID} = ?
        '''
        list = db_helper.execute_query(sql, (car_id,))
        return len(list) > 0

    def search(self, car_id:int) -> dict:
        '''
        To look up a car's information.
        '''

        if not car_id: 
            raise DBExeError("Must provide car_id while invoking exist() from CarTable.")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.ID} = ?
        '''
        list = db_helper.execute_query(sql, (car_id,))
        if len(list) == 0:
            raise CarError(ServErrorCode.CarNotExist, 'Car undefined.')

        return dict(list[0])
    
    def search_for_users(self, user_id:int, order:str) -> list[dict]:
        '''
        To look up a car's information.
        '''

        if user_id is None: 
            raise DBExeError("Must provide car_id while invoking exist() from CarTable.")

        order_by = order if order else ''

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.USER_ID} = ? {order_by}
        '''
        list = db_helper.execute_query(sql, (user_id,))
        ret = []
        for row in list:
            ret.append(dict(row))

        return ret

        
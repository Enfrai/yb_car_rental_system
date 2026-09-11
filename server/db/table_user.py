'''
Definition and implementation for user table.
@author shuohui liu
@date 10 Sep 2026
'''

from enum import Enum
from .db_helper import db_helper, DBHelper
from exception.user_error import UserError, ServErrorCode

class Columns(Enum):
    ID = 'user_id'
    USERNAME = 'username'
    PASSWORD = 'password'
    EMAIL = 'email'
    IS_ADMIN = 'is_admin'
    IS_CUSTOMER = 'is_customer'

_TABLE_NAME = 'users'


class UserTable:
    def __init__(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
                {Columns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Columns.USER_NAME} CHAR(64) NOT NULL,
                {Columns.PASSWORD} CHAR(128) NOT NULL,
                {Columns.EMAIL} CHAR(128) NOT NULL,
                {Columns.IS_ADMIN} BOOLEAN NOT NULL,
                {Columns.IS_CUSTOMER} BOOLEAN NOT NULL
            )
            '''
        db_helper.execute_non_query(sql)

    def update(self, user_id: int, username: str, email: str, password: str, is_admin: bool, is_customer: bool) -> bool:
        '''
        update user info by user_id
        '''

        cols = []
        vals = ()
        if not username:
            cols.append(Columns.USERNAME + ' = ?')
            vals += (username,)

        if not email:
            cols.append(Columns.EMAIL + ' = ?')
            vals += (email,)

        if not password:
            cols.append(Columns.PASSWORD + ' = ?')
            vals += (password,)

        if not is_admin:
            cols.append(Columns.IS_ADMIN + ' = ?')
            vals += (is_admin,)

        if not is_customer:
            cols.append(Columns.IS_CUSTOMER + ' = ?')
            vals += (is_customer,)

        if len(cols) == 0:
            return True
        
        sql = f'''
            UPDATE {_TABLE_NAME} 
            SET {", ".join(cols)}
            WHERE {Columns.ID} = ?
        '''
        if db_helper.execute_non_query(sql, vals) == 0:
            # True
            db_helper.commit()
            return True
        else:
            db_helper.rollback()
            return False


    def insert(self, username: str, email: str, password: str, is_admin: bool, is_customer: bool) -> bool:
        '''
        insert on record into user table
        '''

        if not username or not email or not password or not is_admin is None or is_customer is None:
            raise UserError(ServErrorCode.UserInfoMissed, 'Info missed while registering a user.')

        sql = f'''
                INSERT INTO {_TABLE_NAME} 
                ({Columns.USERNAME}, {Columns.PASSWORD}, {Columns.EMAIL}, {Columns.IS_ADMIN}, {Columns.IS_CUSTOMER})
                values 
                (?, ?, ?, ?, ?)
            '''
        ret = db_helper.execute_non_query(sql, (username, password, email, is_admin, is_customer))
        if ret == 0:
            # True
            db_helper.commit()
            return True
        else:
            db_helper.rollback
            return False

    def exist(self, email: str = None, user_id: int = None) -> bool:
        '''
        To ensure if a user identified by email or user_id is exist.
        '''

        condition = ''
        values = ()
        if user_id is not None:
            condition = f'{Columns.ID} = ?'
            values = (user_id,)
        elif email is not None:
            condition = f'{Columns.EMAIL} = ?'
            values = (email,)
        else:
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide email or user_id while invoking exist().")
        
        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {condition}
        '''

        list = db_helper.execute_query(sql, sql, values)
        return len(list) > 0

    def search_by_id(self, user_id:int) -> dict:
        '''
        To look for a user according to user id. And return all info as dictionary
        '''

        if user_id is None:
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide user_id while invoking search_by_id().")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.ID} = ?
        '''

        list = db_helper.execute_query(sql, sql, (user_id,))
        if len(list) == 0:
            raise UserError(ServErrorCode.UserNotExist, 'User undefined')

        return dict(list[0])

    def search_by_email(self, email:str) -> dict:
        '''
        To look for a user according to user id. And return all info as dictionary
        '''

        if email is None:
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide user_id while invoking search_by_id().")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.email} = ?
        '''

        list = db_helper.execute_query(sql, sql, (email,))
        if len(list) == 0:
            raise UserError(ServErrorCode.UserNotExist, 'User undefined')

        return dict(list[0])

    def search_by_email_and_password(self, email:str, password:str) -> dict:
        '''
        To look for a user according to email & password. And return all info as dictionary
        '''

        if email is None or password is None:
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide user_id while invoking search_by_email_and_password().")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.EMAIL} = ? AND {Columns.PASSWORD} = ?
        '''

        list = db_helper.execute_query(sql, sql, (email, password))
        if len(list) == 0:
            raise UserError(ServErrorCode.UserNotExist, 'No matched user by email and password.')

        return dict(list[0])


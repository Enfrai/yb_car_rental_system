'''
Definition and implementation for user table.
@author shuohui liu
@date 10 Sep 2026
'''

from enum import Enum
from .db_helper import db_helper, DBHelper
from exception.user_error import UserError, ServErrorCode
from lib import Logger

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
                {Columns.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Columns.USERNAME.value} CHAR(64) NOT NULL,
                {Columns.PASSWORD.value} CHAR(128) NOT NULL,
                {Columns.EMAIL.value} CHAR(128) NOT NULL,
                {Columns.IS_ADMIN.value} BOOLEAN NOT NULL,
                {Columns.IS_CUSTOMER.value} BOOLEAN NOT NULL
            )
            '''
        db_helper.execute_non_query(sql)
        db_helper.commit()

    def _row_to_dict(self, row) -> dict:
        return {
            Columns.ID.value: row[0],
            Columns.USERNAME.value: row[1],
            Columns.PASSWORD.value: row[2],
            Columns.EMAIL.value: row[3],
            Columns.IS_ADMIN.value: row[4],
            Columns.IS_CUSTOMER.value: row[5],
        }

    def update(self, user_id: int, username: str, email: str, password: str, is_admin: bool, is_customer: bool) -> bool:
        '''
        update user info by user_id
        '''

        cols = []
        vals = ()
        if not username:
            cols.append(Columns.USERNAME.value + ' = ?')
            vals += (username,)

        if not email:
            cols.append(Columns.EMAIL.value + ' = ?')
            vals += (email,)

        if not password:
            cols.append(Columns.PASSWORD.value + ' = ?')
            vals += (password,)

        if not is_admin:
            cols.append(Columns.IS_ADMIN.value + ' = ?')
            vals += (is_admin,)

        if not is_customer:
            cols.append(Columns.IS_CUSTOMER.value + ' = ?')
            vals += (is_customer,)

        if len(cols) == 0:
            return True
        
        sql = f'''
            UPDATE {_TABLE_NAME} 
            SET {", ".join(cols)}
            WHERE {Columns.ID.value} = ?
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

        Logger().debug("[db] insert user: ", f", values: {(username, password, email, is_admin, is_customer)}")

        if not username or not email or not password or is_admin is None or is_customer is None:
            raise UserError(ServErrorCode.UserInfoMissed, 'Info missed while registering a user.')

        sql = f'''
                INSERT INTO {_TABLE_NAME} 
                ({Columns.USERNAME.value}, {Columns.PASSWORD.value}, {Columns.EMAIL.value}, {Columns.IS_ADMIN.value}, {Columns.IS_CUSTOMER.value})
                values 
                (?, ?, ?, ?, ?)
            '''
        
        Logger().debug("[db] insert user: ", f"sql: {sql}")

        ret = db_helper.execute_non_query(sql, (username, password, email, is_admin, is_customer))
        if ret == 0:
            # True
            db_helper.commit()
            Logger().debug("[db] insert user: success")
            return True
        else:
            db_helper.rollback
            Logger().debug("[db] insert user: fail")
            return False

    def exist(self, email: str = None, user_id: int = None) -> bool:
        '''
        To ensure if a user identified by email or user_id is exist.
        '''

        condition = ''
        values = ()
        if user_id is not None:
            condition = f'{Columns.ID.value} = ?'
            values = (user_id,)
        elif email is not None:
            condition = f'{Columns.EMAIL.value} = ?'
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
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.ID.value} = ?
        '''

        list = db_helper.execute_query(sql, sql, (user_id,))
        if len(list) == 0:
            # raise UserError(ServErrorCode.UserNotExist, 'User undefined')
            return None

        return self._row_to_dict(list[0])

    def search_all_users(self, is_admin: bool = False, is_customer: bool = False) -> list[dict]:
        '''
        To search all users by user role
        ''' 
        sql = f'''
            SELECT * FROM {_TABLE_NAME} 
        '''
        conditions = []
        values = ()
        if is_admin:
            conditions.append(f' {Columns.IS_ADMIN.value} = ? ')
            values += (True, )

        if is_customer:
            conditions.append(f' {Columns.IS_CUSTOMER.value} = ? ')
            values += (True, )

        if len(conditions) > 0:
            sql += f' WHERE {' AND '.join(conditions)}'

        rows = db_helper.execute_query(sql, values)
        ret = []
        for r in rows:
            ret.append(self._row_to_dict(r))

        return ret

    def search_by_email(self, email:str) -> dict:
        '''
        To look for a user according to user id. And return all info as dictionary
        '''

        if email is None:
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide user_id while invoking search_by_id().")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.EMAIL.value} = ?
        '''

        rows = db_helper.execute_query(sql, (email,))
        if len(rows) == 0:
            # raise UserError(ServErrorCode.UserNotExist, 'User undefined')
            return None

        return self._row_to_dict(rows[0])

    def search_by_email_and_password(self, email:str, password:str) -> dict:
        '''
        To look for a user according to email & password. And return all info as dictionary
        '''

        if email is None or password is None:
            raise DBExeError(ServErrorCode.ExecuteError, "Must provide user_id while invoking search_by_email_and_password().")

        sql = f'''
            SELECT * FROM {_TABLE_NAME} WHERE {Columns.EMAIL.value} = ? AND {Columns.PASSWORD.value} = ?
        '''

        rows = db_helper.execute_query(sql, (email, password))
        if len(rows) == 0:
            raise UserError(ServErrorCode.UserNotExist, 'No matched user by email and password.')

        return self._row_to_dict(rows[0])


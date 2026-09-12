'''
An implementation of SQLite 
@author shuohui liu
@date 10 Sep 2026
'''

from .database import Database
import sqlite3
from lib import Logger

class SQLiteDatabase(Database):
    connection: sqlite3.Connection

    def _open_db_(self):
        '''
        open database based on specific database platform
        '''
        self.connection = sqlite3.connect(self.db_file)
        Logger().debug("[DB] open database")

    def execute_query(self, query: str, params: tuple) -> list:
        '''
        execute select statement
        '''
        Logger().debug(f"[DB] execute_query: query: {query}, params: {params}")

        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        ret = cursor.fetchall()

        Logger().debug(f"[DB] execute_query: result: {ret}")

        return ret

    def execute_non_query(self, query: str, params: tuple):
        '''
        execute update/insert/delete/create table statement
        '''
        Logger().debug(f"[DB] execute_non_query: query: {query}, params: {params}")

        cursor = self.connection.cursor()
        cursor.execute(query, params or ())

    def rollback(self):
        '''
        execute to rollback all modifications
        '''
        self.connection.rollback()
        Logger().debug("[DB] rollback")

    def commit(self):
        '''
        execute database commit'''
        self.connection.commit()
        Logger().debug("[DB] commit")

    def close(self):
        '''
        close database
        '''
        self.connection.close()
        Logger().debug("[DB] close")
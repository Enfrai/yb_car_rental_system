'''
An implementation of SQLite 
@author shuohui liu
@date 10 Sep 2026
'''

from .database import Database
import sqlite3

class SQLiteDatabase(Database):
    connection: sqlite3.Connection

    def _open_db_(self):
        '''
        open database based on specific database platform
        '''
        self.connection = sqlite3.connect(self.db_file)

    def execute_query(self, query: str, params: tuple) -> list:
        '''
        execute select statement
        '''
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def execute_non_query(self, query: str, params: tuple):
        '''
        execute update/insert/delete/create table statement
        '''
        cursor = self.connection.cursor()
        cursor.execute(query, params)

    def rollback(self):
        '''
        execute to rollback all modifications
        '''
        self.connection.rollback()

    def commit(self):
        '''
        execute database commit'''
        self.connection.commit()

    def close(self):
        '''
        close database
        '''
        self.connection.close()
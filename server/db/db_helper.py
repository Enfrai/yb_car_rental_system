'''
Database helper <<Singleton>>
@author shuohui liu
@date 10 Sep 2026
'''

from .database import Database
from .sqlite_database import SQLiteDatabase
import threading

# database implementation configuration
config = {
    "type": "sqlite"
}

class DBHelper:
    _instance = None
    _db: Database = None
    _lock = threading.Lock()

    def __init__(self):
        global config

        if config['type'] == 'sqlite':
            self._instance = SQLiteDatabase()
        else:
            raise ValueError('Directed to an undefined database type!!')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def execute_query(self, query: str, params: tuple = None) -> list:
        '''
        execute select statement
        '''
        try:
            return self._db.execute_query(query, params)
        except:
            return []

    def execute_non_query(self, query: str, params: tuple = None) -> int:
        '''
        execute update/insert/delete/create table statement'''
        try:
            self._db.execute_non_query(query, params)
            return 0
        except:
            return -1

    def commit(self):
        '''
        execute database commit'''
        self._db.commit()

    def close(self):
        '''
        close database
        '''
        if self._db:
            self._db.close()
            self._db = None

# for outside
db_helper = DBHelper()

def close_database():
    db_helper.close()
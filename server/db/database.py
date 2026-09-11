'''
Database definition
@author shuohui liu
@date 10 Sep 2026
'''

class Database:
    '''
    A abstract database definition for any kind of database, such as SQLite, MySQL etc.
    '''

    db_file = "build/car_rental_system.db"

    def __init__(self, db_file:str = None):
        if db_file != None:
            self.db_file = db_file

        self._open_db_()

    def _open_db_(self):
        '''
        open database based on specific database platform
        '''
        pass

    def execute_query(self, query: str, params: tuple) -> list:
        '''
        execute select statement
        '''
        pass

    def execute_non_query(self, query: str, params: tuple):
        '''
        execute update/insert/delete/create table statement'''
        pass

    def rollback(self):
        '''
        execute rollback
        '''
        pass

    def commit(self):
        '''
        execute database commit'''
        pass

    def close(self):
        '''
        close database
        '''
        pass
    
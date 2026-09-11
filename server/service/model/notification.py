from exception import OnExitNotification, OnExceptionNotification
from db import close_database

class OnDBExitNotification(OnExitNotification):
    def onNotify(self, *args, **kwargs):
       close_database()

class OnDBExceptionNotification(OnExitNotification):
    def onNotify(self, *args, **kwargs):
       close_database()
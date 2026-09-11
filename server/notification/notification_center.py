from exception import OnExitNotification, OnExceptionNotification

class NotificationCenter:
    exit_listeners: set[OnExitNotification]
    except_listeners: set[OnExceptionNotification]

    def __init__(self):
        self.exit_listeners = set([])
        self.except_listeners = set([])

    def register(self, listener: (OnExceptionNotification | OnExitNotification)):
        if isinstance(listener, OnExitNotification):
            self.exit_listeners.add(listener)
        elif isinstance(listener, OnExceptionNotification):
            self.except_listeners.add(listener)
        return self        

    def notify_exit(self, *args, **kwargs):
        if not self.exit_listeners:
            return

        for l in self.exit_listeners:
            l.onNotify(args, kwargs)

    def notify_exception(self, *args, **kwargs):
        if not self.except_listeners:
            return

        for l in self.except_listeners:
            l.onNotify(args, kwargs)
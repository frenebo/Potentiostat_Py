import time

class AbstractLogger:
    def log(self, text):
        raise NotImplementedError()

class PrintLogger(AbstractLogger):
    def __init__(self):
        pass
    
    def log(self, text):
        print(text)
    
    def error(self, text):
        print(text)

class CallbackLogger(AbstractLogger):
    def __init__(self):
        self._on_log_listeners = []
        self._on_error_listeners = []
        pass
    
    def on_log(self, callback):
        self._on_log_listeners.append(callback)
    
    def on_error(self, callback):
        self._on_error_listeners.append(callback)
    
    def error(self, text):
        time_logged_seconds = time.time()
        for l in self._on_error_listeners:
            l(text, time_logged_seconds)
    
    def log(self, text):
        time_logged_seconds = time.time()
        for l in self._on_log_listeners:
            l(text, time_logged_seconds)
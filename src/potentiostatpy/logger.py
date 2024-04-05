import time

class AbstractLogger:
    def log(self, text):
        raise NotImplementedError()

class PrintLogger(AbstractLogger):
    def __init__(self):
        pass
    
    def log(self, text):
        print(text)

class CallbackLogger(AbstractLogger):
    def __init__(self):
        self.on_log_listeners = []
        pass
    
    def on_log(self, callback):
        self.on_log_listeners.append(callback)
    
    def log(self, text):
        time_logged_seconds = time.time()
        for l in self.on_log_listeners:
            l(text, time_logged_seconds)


class AbstractLogger:
    def log(self, text):
        raise NotImplementedError()

class PrintLogger(Logger):
    def __init__(self):
        pass
    
    def log(self, text):
        print(text)

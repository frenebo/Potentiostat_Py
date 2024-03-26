

class AbstractLogger:
    def log(self, text):
        raise NotImplementedError()

class PrintLogger(AbstractLogger):
    def __init__(self):
        pass
    
    def log(self, text):
        print(text)

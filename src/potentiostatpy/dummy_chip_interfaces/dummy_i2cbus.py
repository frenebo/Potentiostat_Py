# import smbus

def dummy_get_bus():
    return DummySMBus()
    # return smbus.SMBus(1)


class DummySMBus:
    def __init__(self):
        pass
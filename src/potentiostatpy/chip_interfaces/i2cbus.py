import smbus

def get_bus():
    return smbus.SMBus(1)
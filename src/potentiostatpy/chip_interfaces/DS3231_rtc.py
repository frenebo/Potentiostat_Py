from ..logger import PrintLogger


class DS3231RealTimeClockInterface:
    """
    Represents the real-time-clock chip present on the base PCB of the potentiostat. Contains functions
    for interacting with the real time clock.
    """
    def __init__(self, bus, i2c_address: int, logger=PrintLogger()):
        self.bus = bus
        self.address = i2c_address
        self.l = logger
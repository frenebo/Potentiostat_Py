import math

from ..logger import PrintLogger
import numpy as np


class DummyADS1015ADCInterface:
    PGA_6_144V = 0
    PGA_4_096V = 1
    PGA_2_048V = 2
    PGA_1_024V = 4
    PGA_0_512V = 8
    PGA_0_256V = 16

    def __init__(self, bus, i2c_address: int, module_idx, module_i2c_multiplexer, logger=PrintLogger()):
        self.bus = bus
        self.address = i2c_address
        self.module_idx = module_idx
        self.multiplexer = module_i2c_multiplexer
        self.l = logger
        self._adcBits = 12
        self._maxPorts = 4
        self._gain_id = self.PGA_4_096V

        self._dummy_true_voltage = 1.8
        self._reading_noise_sigma = 0.05
        
    def readADC(self, pin: int) :
        "Get ADC value of a pin"
        if (pin >= self._maxPorts or pin < 0) : raise Exception("Invalid pin no {}".format(pin))

        reading_voltage = self._dummy_true_voltage + np.random.normal(0, self._reading_noise_sigma, 1)[0]

        # raise Exception("Unimplemented!")
        return math.floor(  (reading_voltage / self.getMaxVoltage() ) * (2 ** (self._adcBits - 1) - 1))
        # self.requestADC(pin)
        # return self._getADC()
    
    def getMaxVoltage(self) -> float :
        "Get maximum voltage conversion range"
        if self._gain_id == self.PGA_6_144V : return 6.144
        elif self._gain_id == self.PGA_4_096V : return 4.096
        elif self._gain_id == self.PGA_2_048V : return 2.048
        elif self._gain_id == self.PGA_1_024V : return 1.024
        elif self._gain_id == self.PGA_0_512V : return 0.512
        elif self._gain_id == self.PGA_0_256V: return 0.256
        else : raise Exception("Invalid gain id itnernal value {}".format(self._gain_id))

    def setGain(self, gain_id: int) :
        assert gain_id in [
            self.PGA_6_144V,
            self.PGA_4_096V,
            self.PGA_2_048V,
            self.PGA_1_024V,
            self.PGA_0_512V,
            self.PGA_0_256V,
        ], "When setting gain, should pick one of the magic numbers..."
        self._gain_id = gain_id
    
    def toVoltage(self, value: int = 1) -> float :
        "Transform an ADC value to nominal voltage"
        volts = self.getMaxVoltage() * value
        return volts / ((2 ** (self._adcBits - 1)) - 1)
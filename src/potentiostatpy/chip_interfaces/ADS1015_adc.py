from ..logger import PrintLogger



class ADS1015ADCInterface:
    
    def get_voltage(self, adc_subchannel_idx):
        self.module_multiplexer.select_module(self.module_idx)

        print("Here this should look at voltage from subchannel idx {}".format(adc_subchannel_idx))
        raise NotImplementedError()
    
    # @TODO
    def set_gain(self, gain):
        self.module_multiplexer.select_module(self.module_idx)
        raise NotImplementedError()
    
    def set_single_channel_voltage(self, channel_idx: int, voltage: float):
        assert channel_idx in [0,1,2,3]

        self.module_multiplexer.select_module(self.module_idx)
        raise NotImplementedError()
        # self.



"""
This code is adapted from Chandra Wijaya Sentosa's code at https://github.com/chandrawi/ADS1x15-ADC
The license for the original code is included below:

Copyright (c) 2012 Chandra Wijaya Sentosa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""



import time


class ADS1015ADCInterface:
    "ADS1015 ADC class to be used with the TCA9548AMultiplexerInterface"

    # ADS1x15 register address
    CONVERSION_REG = 0x00
    CONFIG_REG     = 0x01
    LO_THRESH_REG  = 0x02
    HI_THRESH_REG  = 0x03


    # Programmable gain amplifier configuration
    PGA_6_144V = 0
    PGA_4_096V = 1
    PGA_2_048V = 2
    PGA_1_024V = 4
    PGA_0_512V = 8
    PGA_0_256V = 16


    def __init__(self, bus, i2c_address: int, module_idx, module_i2c_multiplexer, logger=PrintLogger()):
        "Initialize ADS1015 with SMBus ID and I2C address configuration"
        self._i2cbus = bus
        self._address = i2c_address
        self._module_idx = module_idx
        self._module_i2c_multiplexer
        self._l = logger
        self._conversionDelay = 2
        self._maxPorts = 4
        self._adcBits = 12
        # Store initial config resgister to config property
        self._config = self._readRegister(self.CONFIG_REG)

    def _writeRegister(self, address: int, value) :
        "Write 16-bit integer to an address pointer register"
        registerValue = [(value >> 8) & 0xFF, value & 0xFF]
        self._i2cbus.write_i2c_block_data(self._address, address, registerValue)

    def _readRegister(self, address: int) :
        "Read 16-bit integer value from an address pointer register"
        registerValue = self._i2cbus.read_i2c_block_data(self._address, address, 2)
        return (registerValue[0] << 8) + registerValue[1]

    def setInput(self, input: int) :
        "Set input multiplexer configuration"
        # Filter input argument
        if input < 0 or input > 7 : inputRegister = 0x0000
        else : inputRegister = input << 12
        # Masking input argument bits (bit 12-14) to config register
        self._config = (self._config & 0x8FFF) | inputRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getInput(self) :
        "Get input multiplexer configuration"
        return (self._config & 0x7000) >> 12

    def setGain(self, gain: int) :
        "Set programmable gain amplifier configuration"
        # Filter gain argument
        if gain == self.PGA_4_096V : gainRegister = 0x0200
        elif gain == self.PGA_2_048V : gainRegister = 0x0400
        elif gain == self.PGA_1_024V : gainRegister = 0x0600
        elif gain == self.PGA_0_512V : gainRegister = 0x0800
        elif gain == self.PGA_0_256V : gainRegister = 0x0A00
        else : gainRegister = 0x0000
        # Masking gain argument bits (bit 9-11) to config register
        self._config = (self._config & 0xF1FF) | gainRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getGain(self) :
        "Get programmable gain amplifier configuration"
        gainRegister = self._config & 0x0E00
        if gainRegister == 0x0200 : return self.PGA_4_096V
        elif gainRegister == 0x0400 : return self.PGA_2_048V
        elif gainRegister == 0x0600 : return self.PGA_1_024V
        elif gainRegister == 0x0800 : return self.PGA_0_512V
        elif gainRegister == 0x0A00 : return self.PGA_0_256V
        else : return 0x0000

    def setMode(self, mode: int) :
        "Set device operating mode configuration"
        # Filter mode argument
        if mode == 0 : modeRegister = 0x0000
        else : modeRegister = 0x0100
        # Masking mode argument bit (bit 8) to config register
        self._config = (self._config & 0xFEFF) | modeRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getMode(self) :
        "Get device operating mode configuration"
        return (self._config & 0x0100) >> 8

    def setDataRate(self, dataRate: int) :
        "Set data rate configuration"
        # Filter dataRate argument
        if dataRate < 0 or dataRate > 7 : dataRateRegister = 0x0080
        else : dataRateRegister = dataRate << 5
        # Masking dataRate argument bits (bit 5-7) to config register
        self._config = (self._config & 0xFF1F) | dataRateRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getDataRate(self) :
        "Get data rate configuration"
        return (self._config & 0x00E0) >> 5

    def setComparatorMode(self, comparatorMode: int) :
        "Set comparator mode configuration"
        # Filter comparatorMode argument
        if comparatorMode == 1 : comparatorModeRegister = 0x0010
        else : comparatorModeRegister = 0x0000
        # Masking comparatorMode argument bit (bit 4) to config register
        self._config = (self._config & 0xFFEF) | comparatorModeRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getComparatorMode(self) :
        "Get comparator mode configuration"
        return (self._config & 0x0010) >> 4

    def setComparatorPolarity(self, comparatorPolarity: int) :
        "Set comparator polarity configuration"
        # Filter comparatorPolarity argument
        if comparatorPolarity == 1 : comparatorPolarityRegister = 0x0008
        else : comparatorPolarityRegister = 0x0000
        # Masking comparatorPolarity argument bit (bit 3) to config register
        self._config = (self._config & 0xFFF7) | comparatorPolarityRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getComparatorPolarity(self) :
        "Get comparator polarity configuration"
        return (self._config & 0x0008) >> 3

    def setComparatorLatch(self, comparatorLatch: int) :
        "Set comparator polarity configuration"
        # Filter comparatorLatch argument
        if comparatorLatch == 1 : comparatorLatchRegister = 0x0004
        else : comparatorLatchRegister = 0x0000
        # Masking comparatorPolarity argument bit (bit 2) to config register
        self._config = (self._config & 0xFFFB) | comparatorLatchRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getComparatorLatch(self) :
        "Get comparator polarity configuration"
        return (self._config & 0x0004) >> 2

    def setComparatorQueue(self, comparatorQueue: int) :
        "Set comparator queue configuration"
        # Filter comparatorQueue argument
        if comparatorQueue < 0 or comparatorQueue > 3 : comparatorQueueRegister = 0x0002
        else : comparatorQueueRegister = comparatorQueue
        # Masking comparatorQueue argument bits (bit 0-1) to config register
        self._config = (self._config & 0xFFFC) | comparatorQueueRegister
        self._writeRegister(self.CONFIG_REG, self._config)

    def getComparatorQueue(self) :
        "Get comparator queue configuration"
        return (self._config & 0x0003)

    def setComparatorThresholdLow(self, threshold: float) :
        "Set low threshold for voltage comparator"
        self._writeRegister(self.LO_THRESH_REG, round(threshold))

    def getComparatorThresholdLow(self) :
        "Get voltage comparator low threshold"
        threshold = self._readRegister(self.LO_THRESH_REG)
        if threshold >= 32768 : threshold = threshold - 65536
        return threshold

    def setComparatorThresholdHigh(self, threshold: float) :
        "Set high threshold for voltage comparator"
        self._writeRegister(self.HI_THRESH_REG, round(threshold))

    def getComparatorThresholdHigh(self) :
        "Get voltage comparator high threshold"
        threshold = self._readRegister(self.HI_THRESH_REG)
        if threshold >= 32768 : threshold = threshold - 65536
        return threshold

    def isReady(self) :
        "Check if device currently not performing conversion"
        value = self._readRegister(self.CONFIG_REG)
        return bool(value & 0x8000)

    def isBusy(self) :
        "Check if device currently performing conversion"
        return not self.isReady()

    def _requestADC(self, input) :
        "Private method for starting a single-shot conversion"
        self.setInput(input)
        # Set single-shot conversion start (bit 15)
        if self._config & 0x0100 :
            self._writeRegister(self.CONFIG_REG, self._config | 0x8000)

    def _getADC(self) -> int :
        "Get ADC value with current configuration"
        t = time.time()
        isContinuos = not (self._config & 0x0100)
        # Wait conversion process finish or reach conversion time for continuous mode
        while not self.isReady() :
            if ((time.time() - t) * 1000) > self._conversionDelay and isContinuos :
                break
        return self.getValue()

    def getValue(self) -> int :
        "Get ADC value"
        value = self._readRegister(self.CONVERSION_REG)
        # Shift bit based on ADC bits and change 2'complement negative value to negative integer
        value = value >> (16 - self._adcBits)
        if value >= (2 ** (self._adcBits - 1)) : value = value - (2 ** (self._adcBits))
        return value

    def requestADC(self, pin: int) :
        "Request single-shot conversion of a pin to ground"
        if (pin >= self._maxPorts or pin < 0) : raise Exception("Invalid pin no {}".format(pin))
        self._requestADC(pin + 4)

    def readADC(self, pin: int) :
        "Get ADC value of a pin"
        if (pin >= self._maxPorts or pin < 0) : raise Exception("Invalid pin no {}".format(pin))
        self.requestADC(pin)
        return self._getADC()

    def getMaxVoltage(self) -> float :
        "Get maximum voltage conversion range"
        if self._config & 0x0E00 == 0x0000 : return 6.144
        elif self._config & 0x0E00 == 0x0200 : return 4.096
        elif self._config & 0x0E00 == 0x0400 : return 2.048
        elif self._config & 0x0E00 == 0x0600 : return 1.024
        elif self._config & 0x0E00 == 0x0800 : return 0.512
        else : return 0.256

    def toVoltage(self, value: int = 1) -> float :
        "Transform an ADC value to nominal voltage"
        volts = self.getMaxVoltage() * value
        return volts / ((2 ** (self._adcBits - 1)) - 1)

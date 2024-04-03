# This code is copied from the Pansodtee et al. supplementary materials for their potentiostat.


"""
================================================
MCP4728 DAC

Marko Pinteric 2018
http://www.pinteric.com/raspberry.html

Requires python smbus to be installed
================================================
"""

# import smbus

# import RPi.GPIO as GPIO
# import re
# import platform
# import time
from ..logger import PrintLogger

class MCP4728:
    """
    Control the MCP4728 DAC
    """
    # internal variables
    # __dac_address = 0x60
    # __bus = None

    def __updatebyte(self, byte, mask, value):
        byte &= mask
        byte |= value
        return byte

    # init object with i2caddress, default is 0x60 for MCP4728
    def __init__(self, bus, i2c_address=0x60, module_idx, module_multiplexer, logger=PrintLogger()):
        self.__bus = bus
        self.__dac_address = i2c_address
        self.__module_idx = module_idx
        self.__module_multiplexer = module_multiplexer
        self.__l = logger

        
    # def verify_connection(self):
    #     raise NotImplementedError()
    
    # # @TODO delete this function? needed?
    # def reset(self):
    #     self.module_multiplexer.select_module(self.module_idx)
    #     data = 0x06
    #     register =0x00
    #     self.l.log("Resetting DAC: Writing {dat:#010b} to register {reg:#010b} at address {addr:#010b}".format(dat=data, reg=register, addr=self.address))
    #     self.bus.write_byte_data(self.address, register, data)
    
    # def set_voltage(self, channel, value):
    #     self.module_multiplexer.select_module(self.module_idx)
    #     raise NotImplementedError()


    def _single_raw(self, channel, reference, gain, value):
        """
        writes single raw value to the selected DAC channel - channels 1 to 4
        """
        second, third = divmod(value, 0x100)
        first=self.__updatebyte(0x58,0xFF,(channel-1) << 1)
        second=self.__updatebyte(second,0x0F,reference << 7 | gain << 4)
        self.__module_multiplexer.select_module(self.__module_idx)
        self.__bus.write_i2c_block_data(self.__dac_address,first,[second, third])

    def set_voltage(self, channel, volt):
        """
        writes single value to the selected DAC channel using internal reference - channels 1 to 4
        """
        if volt>2: gain=2
        else: gain=1
        value=int(0x1000 * volt/2.048/gain)
        self._single_raw(channel,1,gain-1,value)

    # # @TODO delete this function? needed?
    # def reset(self):
    #     self.module_multiplexer.select_module(self.module_idx)
    #     data = 0x06
    #     register =0x00
    #     self.l.log("Resetting DAC: Writing {dat:#010b} to register {reg:#010b} at address {addr:#010b}".format(dat=data, reg=register, addr=self.address))
    #     self.bus.write_byte_data(self.address, register, data)
    

    # def single_external(self, channel, rel):
    #     """
    #     writes single value to the selected DAC channel using external reference - channels 1 to 4
    #     """
    #     value=int(0x1000 * rel)
    #     self.single_raw(channel,0,0,value)


# class MCP4728_address:
#     """
#     Gets and sets the MCP4728 DAC address
#     """
#     # local methods
#     # all assume and leave SCL low, except when specified differently
    
#     # assumes SCL and SDA high
#     def __i2cstart(self):
#         GPIO.setup(self.__sda_gpio, GPIO.OUT, initial=GPIO.LOW)
#         GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)

#     def __i2crestart(self):
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__sda_gpio, GPIO.OUT, initial=GPIO.LOW)
#         GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)

#     # leaves SCL and SDA high
#     def __i2cstop(self):
#         GPIO.setup(self.__sda_gpio, GPIO.OUT, initial=GPIO.LOW)
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__sda_gpio, GPIO.IN)

#     def __i2cgetbyte(self):
#         num=0x00
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         for i in range(8):
#             GPIO.setup(self.__scl_gpio, GPIO.IN)
#             # clock stretching
#             while(GPIO.input(self.__scl_gpio)==False): time.sleep(0.000001)
#             num = num << 1
#             if(GPIO.input(self.__sda_gpio)==True): num = num | 0x01
#             GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)
#         #print('Getting: {0:08b}'.format( num )) # for testing purposes
#         return(num)

#     def __i2csendbyte(self,num):
#         #print('Sending: {0:08b}'.format( num )) # for testing purposes
#         for i in range(8):
#             if num & 0x80 == 0:
#                 GPIO.setup(self.__sda_gpio, GPIO.OUT, initial=GPIO.LOW)
#             else:
#                 GPIO.setup(self.__sda_gpio, GPIO.IN)
#             num = num << 1
#             GPIO.setup(self.__scl_gpio, GPIO.IN)
#             GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)

#     def __i2cgetack(self):
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         res=GPIO.input(self.__sda_gpio)
#         GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)
#         return(not res)

#     def __i2csendack(self):
#         GPIO.setup(self.__sda_gpio, GPIO.OUT, initial=GPIO.LOW)
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)

#     def __i2csendnack(self):
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__scl_gpio, GPIO.OUT, initial=GPIO.LOW)

#     # init object with GPIO addresses
#     def __init__(self, scl, sda, ldac):
#         self.__scl_gpio=scl
#         self.__sda_gpio=sda
#         self.__ldac_gpio=ldac
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)

#     def getaddress(self):
#         """
#         gets the DAC address
#         """
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         GPIO.setup(self.__ldac_gpio, GPIO.IN)

#         self.__i2cstart()
#         self.__i2csendbyte(0)
#         if(self.__i2cgetack()==False): print('No ACK G1')
#         self.__i2csendbyte(0x0C)
#         GPIO.setup(self.__ldac_gpio, GPIO.OUT, initial=GPIO.LOW)
#         if(self.__i2cgetack()==False): print('No ACK G2')
#         self.__i2crestart()
#         self.__i2csendbyte(0xC1)
#         GPIO.setup(self.__ldac_gpio, GPIO.IN)
#         if(self.__i2cgetack()==False): print('No ACK G3')
#         val = self.__i2cgetbyte()
#         self.__i2csendnack()
#         self.__i2cstop()
#         adr1 = (val & 0xE0) >> 5
#         adr2 = (val & 0x0E) >> 1
#         if ((adr1 != adr2) or ((val & 0x11) != 0x10)):
#             print('Error: returned {0:08b}'.format(val))
#         return(0xC0 | adr1)

#     def setaddress(self,cur,new):
#         """
#         sets the DAC address
#         """
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         GPIO.setup(self.__ldac_gpio, GPIO.IN)
#         cur &= 0x07
#         new &= 0x07

#         self.__i2cstart()
#         self.__i2csendbyte(0xC0 | (cur << 1))
#         if(self.__i2cgetack()==False): print('No ACK S1')
#         self.__i2csendbyte(0x61 | (cur << 2))
#         GPIO.setup(self.__ldac_gpio, GPIO.OUT, initial=GPIO.LOW)
#         if(self.__i2cgetack()==False): print('No ACK S2')
#         self.__i2csendbyte(0x62 | (new << 2))
#         if(self.__i2cgetack()==False): print('No ACK S3')
#         self.__i2csendbyte(0x63 | (new << 2))
#         GPIO.setup(self.__ldac_gpio, GPIO.IN)
#         if(self.__i2cgetack()==False): print('No ACK S4')
#         self.__i2cstop()

#     def reset(self):
#         """
#         resets the DAC
#         """
#         GPIO.setup(self.__scl_gpio, GPIO.IN)
#         GPIO.setup(self.__sda_gpio, GPIO.IN)
#         GPIO.setup(self.__ldac_gpio, GPIO.IN)

#         self.__i2cstart()
#         self.__i2csendbyte(0x00)
#         if(self.__i2cgetack()==False): print('No ACK R1')
#         self.__i2csendbyte(0x06)
#         if(self.__i2cgetack()==False): print('No ACK R2')
#         self.__i2cstop()

from ..logger import PrintLogger


class MCP4728DACInterface:
    """
    Interface for the MCP4728 DAC. Creating this class doesn't automatically send data
    or change the device, this just provides a convenient class to do things with the DAC.

    NOTE: If the i2c multiplexer selects a different board, this class will not notice, and will point towards
    the new board's dac without any warning.
    """

    def __init__(self, bus, i2c_address, logger=PrintLogger()):
        self.bus = bus
        self.address = i2c_address
        self.l = logger
    
    def reset():
        data = 0x06
        register =0x00
        self.l.log("Resetting DAC: Writing {dat:#010b} to register {reg:#010b} at address {addr:#010b}".format(dat=data, reg=register, addr=self.address))
        self.bus.write_byte_data(self.address, register, data)
    
    def set_voltage(channel, value):
        raise NotImplementedError()
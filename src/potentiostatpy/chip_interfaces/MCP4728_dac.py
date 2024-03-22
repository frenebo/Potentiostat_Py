


class MCP4728DACInterface:
    """
    Interface for the MCP4728 DAC. Creating this class doesn't automatically send data
    or change the device, this just provides a convenient class to do things with the DAC.

    NOTE: If the i2c multiplexer selects a different board, this class will not notice, and will point towards
    the new board's dac without any warning.
    """

    def __init__(self, bus, i2c_address):
        self.bus = bus
        self.address = i2c_address
    
    def reset():
        self.bus.write_byte_data(self.address, 0x00, 0x06)
    
    def set_voltage(channel, value):
        raise NotImplementedError()
from ..logger import PrintLogger

class DummyMCP4728DACInterface:
    def __updatebyte(self, byte, mask, value):
        byte &= mask
        byte |= value
        return byte

    # init object with i2caddress, default is 0x60 for MCP4728
    def __init__(self, bus, i2c_address, module_idx, module_multiplexer, logger=PrintLogger()):
        self.__bus = bus
        self.__dac_address = i2c_address
        self.__module_idx = module_idx
        self.__module_multiplexer = module_multiplexer
        self.__l = logger


    def _single_raw(self, channel, reference, gain, value):
        pass
        # """
        # writes single raw value to the selected DAC channel - channels 1 to 4
        # """
        # second, third = divmod(value, 0x100)
        # first=self.__updatebyte(0x58,0xFF,(channel-1) << 1)
        # second=self.__updatebyte(second,0x0F,reference << 7 | gain << 4)
        # self.__module_multiplexer.select_module(self.__module_idx)
        # self.__bus.write_i2c_block_data(self.__dac_address,first,[second, third])

    def set_voltage(self, channel, volt):
        pass
        # """
        # writes single value to the selected DAC channel using internal reference - channels 1 to 4
        # """
        # if volt>2: gain=2
        # else: gain=1
        # value=int(0x1000 * volt/2.048/gain)
        # self._single_raw(channel,1,gain-1,value)

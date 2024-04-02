from ..logger import PrintLogger

class ADS1015ADCInterface:
    def __init__(self, bus, i2c_address: int, module_idx: int, module_multiplexer, logger=PrintLogger()):
        self.bus = bus
        self.address = i2c_address
        self.module_idx = module_idx
        self.module_multiplexer = module_multiplexer
        self.l = logger

    
    def get_voltages(self, adc_subchannel_idx):
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
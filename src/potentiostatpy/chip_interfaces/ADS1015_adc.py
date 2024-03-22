
class ADS1015ADCInterface:
    def __init__(self, bus, i2c_address: int):
        self.bus = bus
        self.address = i2c_address
    
    def set_voltages(self, v0:float, v1:float, v2:float, v3:float):
        raise NotImplementedError()
    
    # @TODO
    def set_gain(self, gain):
        raise NotImplementedError()
    
    def set_single_channel_voltage(self, channel_idx: int, voltage: float):
        assert channel_idx in [0,1,2,3]

        raise NotImplementedError()
        # self.
import smbus


class Potentiostat:
    """
    Class to communicate with and keep track of the different chips
    of the potentiostat's board and stack modules
    """
    def __init__(self, n_modules: int):
        self.n_modules = n_modules
    
    def set_channel_voltage(self, channel_idx, voltage):
        raise NotImplementedError()
    
    def set_channel_voltages(self, channel_indices, channel_voltages):
        assert len(channel_indices) == len(channel_voltages)

        for i in range(len(channel_indices)):
            chan_idx = channel_indices[i]
            chan_voltage = channel_voltages[i]
            self.set_channel_voltage(chan_idx, chan_voltage)
    
    def check_potentiostat(self):
        raise NotImplementedError()

        # Check DS3231 real-time clock 

        # Check module multiplexer 

        # For each module, check that all chips are found
        for i in range(self.n_modules):
            pass
            # Check MCP4728
            # Check ADS1015 ADC
            # Check 
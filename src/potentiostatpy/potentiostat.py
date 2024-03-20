import smbus


class Potentiostat:
    """
    Class to communicate with and keep track of the different chips
    of the potentiostat's board and stack modules
    """
    def __init__(self, n_modules: int):
        self.n_modules = n_modules
    
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
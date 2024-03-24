import smbus
from chip_interfaces.DS3231_rtc import DS3231RealTimeClockInterface
from chip_interfaces.MCP4728_dac import MCP4728DACInterface
from chip_interfaces.ADS1015_adc import ADS1015ADCInterface

TCA9548A_DEFAULT_ADDRESS = 0x77
DS3231_ADDRESS = 0x68

ADS_0_STACK_ADDR = 0b1001001
ADS_1_STACK_ADDR = 0b1001000


class Potentiostat:
    """
    Class to communicate with and keep track of the different chips
    of the potentiostat's board and stack modules

    n_modules: int - number of stack PCBs connected - 8 channels each, max of 8 for tot. 64 channels

    """
    def __init__(self, n_modules: int):
        self.n_modules = n_modules

        self.channel_voltages = [None] * self.n_channels
        self.connected_channels = [None] * self.n_channels

        self.i2c_multiplexer = TCA9548MultiplexerInterface(self.bus, self.n_modules, TCA9548A_DEFAULT_ADDRESS, logging=True)
        self.rtc = DS3231RealTimeClockInterface(self.bus, DS3231_ADDRESS)

        # @TODO implement some kind of calibration for the Vref and 1V65, which have trouble when it comes to the trimpots
        raise NotImplementedError()

        # self.check_potentiostat()

        # self.reset_channel_switches()
        # self.reset_channel_voltages()
    
    """
    Sets the switches on the modules to "off", disconnecting the voltage outputs of the DACs and op-amps from the electrodes.
    """
    def disconnect_all_electrodes(self):
        for chan_idx in range(self.n_channels):
            self.set_chan_switch(chan_idx, False)
    
    """
    Sets the output voltages of the electrodes to zero. Will only have noticeable effect for the electrodes that are currently "on" and connected.
    """
    def zero_all_voltages(self):
        for chan_idx in range(self.n_channels):
            self.set_chan_voltage(chan_idx, 0.0)

    
    @property
    def n_channels(self):
        return self.n_modules * 8
    
    # """
    # reset_channel_switches

    # Start by switching off all channel switches, isolating electrodes
    # """
    # def reset_channel_switches(self):
    #     for chan_idx in range(self.n_channels):
    #         self.set_chan_switch(chan_idx)
    
    """
    set_chan_switch

    Switches the selected channel either on or off
    """
    def set_chan_switch(self, channel_idx: int, state: bool):
        if channel_idx < 0:
            raise Exception("Invalid negative channel index {}".format(channel_idx))
        if channel_idx >= self.n_channels:
            raise Exception("Invalid channel idx {}. Only {} modules connected, "
                "with 8 channels each. Channel idx must be 0-{}".format(
                channel_idx,
                self.n_modules,
                self.n_channels,
            ))
        if state != True and state != False:
            raise Exception("invalid channel switch state {}, must be boolean True or False".format(state))
        
        # Message the shift register and set the channel on or off
        raise NotImplementedError()

    
    """
    set_chan_voltage

    Sets the selected channel to the selected voltage
    """
    def set_chan_voltage(self, channel_idx: int, voltage: float):
        if channel_idx < 0 or channel_idx >= self.n_channels:
            raise Exception("Invalid channel idx {}. Must be 0 to {}".format(channel, self.n_channels - 1))
        
        module_idx = channel_idx // 8
        module_subchannel_idx = channel_idx % 8

        self.switch_i2cmultiplexer(module_idx)

        raise NotImplementedError()


    """
    switch_i2cmultiplexer

    Uses the I2C multiplexer on the main board to select the given stack board,
    so that the DACs and ADCs on that 8-channel board are available to the
    Raspberry Pi
    """
    def switch_i2cmultiplexer(self, module_idx: int):
        self.i2c_multiplexer.select_module(module_idx)

    
    """
    set_voltages

    Sets the voltages for the selected channels
    """
    def set_voltages(self, channel_indices, channel_voltages):
        assert len(channel_indices) == len(channel_voltages)

        for i in range(len(channel_indices)):
            chan_idx = channel_indices[i]
            chan_voltage = channel_voltages[i]
            self.set_channel_voltage(chan_idx, chan_voltage)
    
    def read_currents(self, channel_indices):
        raise NotImplementedError()
    
    def turn_on_channels(self, channel_indices):
        raise NotImplementedError()
    
    def turn_off_channels(self, channel_indices):
        raise NotImplementedError()
    
    def initialize_potentiostat(self):
        # Check DS3231 real-time clock
        raise NotImplementedError() 

        # # Try using multiplexer
        # for i in range(self.n_modules):
        #     self.i2c_multiplexer.select_module(i)

        # For each module, check that all chips seem to be working
        for i in range(self.n_modules):
            self.i2c_multiplexer.select_module(i)

            # Check the ADS1015 ADCs

            # Check the MCP4728 DACs

        
        #?? Check the shift register and switches?
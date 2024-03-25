import smbus
from chip_interfaces.DS3231_rtc import DS3231RealTimeClockInterface
from chip_interfaces.MCP4728_dac import MCP4728DACInterface
from chip_interfaces.ADS1015_adc import ADS1015ADCInterface
from loggers import PrintLogger

# I2C multiplexer on main board
TCA9548A_DEFAULT_ADDRESS = 0x77

# Real time clock on main board
DS3231_ADDRESS = 0x68

# Analog to digital converters on stack boards
ADS_0_STACK_ADDR = 0b1001001
ADS_1_STACK_ADDR = 0b1001000


# Pins for accessing the shift registers that control the analog switches on the stack boards
SDI_pin = 11 #(gpio 17)
RCLK_pin  = 13 #(gpio 27)
SRCLK_pin = 12 #(gpio 18)


class Potentiostat:
    """
    Class to communicate with and keep track of the different chips
    of the potentiostat's board and stack modules

    n_modules: int - number of stack PCBs connected - 8 channels each, max of 8 for tot. 64 channels

    """
    def __init__(self, n_modules: int, logger=PrintLogger()):
        self.n_modules = n_modules
        self.l = logger

        self.channel_voltages = [None] * self.n_channels
        self.connected_channels = [None] * self.n_channels

        self.l.log("Initializing potentiostat. # of modules: {n_modules}, # of channels: {n_channels}".format(n_modules=self.n_modules, n_channels=self.n_channels))
        self.i2c_multiplexer = TCA9548MultiplexerInterface(self.bus, self.n_modules, TCA9548A_DEFAULT_ADDRESS, logger=self.l)
        self.rtc = DS3231RealTimeClockInterface(self.bus, DS3231_ADDRESS, logger=self.l)
        self.switch_shift_register = SN75HC595NShiftRegister(SDI_pin, RCLK_pin, SRCLK_pin, self.n_channels, logger=self.l)


    """
    Sets the switches on the modules to "off", disconnecting the voltage outputs of the DACs and op-amps from the electrodes.
    """
    def disconnect_all_electrodes(self):
        self.l.log("Disconnecting all electrodes")
        raise NotImplementedError()
        # for chan_idx in range(self.n_channels):
        #     self.set_chan_switch(chan_idx, False)
    
    """
    Sets the output voltages of the electrodes to zero. Will only have noticeable effect for the electrodes that are currently "on" and connected.
    """
    def zero_all_voltages(self):
        self.l.log("Setting all channel voltages to zero")
        indices_to_set = list(range(self.n_channels))
        voltages_to_set = [0] * self.n_channels
        self.set_voltages(indices_to_set, voltages_to_set)

    
    @property
    def n_channels(self):
        return self.n_modules * 8
    
    def get_channel_switch_states(self):
        raise NotImplementedError()

    def get_channel_output_voltages(self):
        raise NotImplementedError()
    
    """
    set_chan_switch

    Switches the selected channel either on or off
    """
    def set_chan_switch(self, channel_idx: int, state: bool):
        # self.l.log9
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
        self.l.log("Setting channel {channel_idx} voltage to {v}".format(channel_idx=channel_idx, v=voltage))
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
        self.l.log("Switching I2C multiplexer to board {module_idx}".format(module_idx=module_idx))
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
    
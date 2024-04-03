import smbus
from. chip_interfaces import (
    DS3231RealTimeClockInterface,
    MCP4728DACInterface,
    ADS1015ADCInterface,
    TCA9548MultiplexerInterface,
    SN74HC595NShiftRegister
)
from .logger import PrintLogger

# I2C multiplexer on main board
TCA9548A_DEFAULT_ADDRESS = 0x70


# Each module in the stack contains ADC and DAC to control and read 8 channels
CHANNELS_PER_MODULE = 8
CHANNELS_PER_ADC = 4
CHANNELS_PER_DAC = 4

# Real time clock on main board
DS3231_ADDRESS = 0x68

# Analog to digital converters on stack boards
ADS_0_STACK_ADDR = 0b1001001
ADS_1_STACK_ADDR = 0b1001000

DAC_0_STACK_ADDR = 0b1100000
DAC_1_STACK_ADDR = 0b1100001
print("TODO: Update DAC_0_STACK_ADDR")


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
        self.n_channels = n_modules * CHANNELS_PER_MODULE

        self.l = logger
        self.state_changed_listeners = []

        self.channel_voltages = [None] * self.n_channels
        self.connected_channels = [None] * self.n_channels

        self.l.log("Setting up I2C bus with smbus.")
        self.bus = smbus.SMBus(1)

        self.l.log("Initializing potentiostat. # of modules: {n_modules}, # of channels: {n_channels}".format(n_modules=self.n_modules, n_channels=self.n_channels))
        self.i2c_multiplexer = TCA9548MultiplexerInterface(self.bus, self.n_modules, TCA9548A_DEFAULT_ADDRESS, logger=self.l)
        self.rtc = DS3231RealTimeClockInterface(self.bus, DS3231_ADDRESS, logger=self.l)
        self.switch_shift_register = SN74HC595NShiftRegister(SDI_pin, RCLK_pin, SRCLK_pin, self.n_channels, logger=self.l)

        self.adc_interfaces = []
        self.dac_interfaces = []

        # Create classes to interface with the different ADCs and DACs. Each one is told
        # which module it belongs to, so that it can manage switching the multiplexer
        for module_idx in range(self.n_modules):
            # module_idx * CHANNELS_PER_MODULE
            adc0_interface = ADS1015ADCInterface(self.bus, ADS_0_STACK_ADDR, module_idx, self.i2c_multiplexer, logger=self.l)
            adc1_interface = ADS1015ADCInterface(self.bus, ADS_1_STACK_ADDR, module_idx, self.i2c_multiplexer, logger=self.l)

            
            # ADS.setGain(ADS.PGA_4_096V)

            self.adc_interfaces.append(adc0_interface)
            self.adc_interfaces.append(adc1_interface)

            dac0_interface = MCP4728DACInterface(self.bus, DAC_0_STACK_ADDR, module_idx, self.i2c_multiplexer, logger=self.l)
            dac1_interface = MCP4728DACInterface(self.bus, DAC_1_STACK_ADDR, module_idx, self.i2c_multiplexer, logger=self.l)

            self.dac_interfaces.append(dac0_interface)
            self.dac_interfaces.append(dac1_interface)



    """
    Sets the switches on the modules to "off", disconnecting the voltage outputs of the DACs and op-amps from the electrodes.
    """
    def disconnect_all_electrodes(self, suppress_state_change=False):
        self.l.log("Disconnecting all electrodes")
        self.set_all_channel_switches([False] * self.n_channels)

        if not suppress_state_change:
            self._state_changed()
    
    def cleanup(self):
        # Let go of the GPIO pins used by the switch_shift_register
        self.switch_shift_register.cleanup()
    
    """
    Sets the output voltages of the electrodes to zero. Will only have noticeable effect for the electrodes that are currently "on" and connected.
    """
    def zero_all_voltages(self, suppress_state_change=False):
        self.l.log("Setting all channel voltages to zero")
        indices_to_set = list(range(self.n_channels))
        voltages_to_set = [0.0] * self.n_channels
        self.set_all_voltages(voltages_to_set, suppress_state_change=True)

        
        if not suppress_state_change:
            self._state_changed()


    # Functions to read state
    
    def get_state(self):
        potentiostat_state = {
            "n_modules": self.n_modules,
            "n_channels": self.n_channels,
            "channel_switch_states": self.get_channel_switch_states(),
            "channel_output_voltages": self.get_channel_output_voltages(),
            "channel_output_current": self.get_channel_output_currents(),
        }

        return potentiostat_state
    def get_channel_switch_states(self):
        return self.connected_channels

    def get_channel_output_voltages(self):
        return self.channel_voltages
    
    def get_channel_output_currents(self):
        # return self.
        chan_currents = [];
        for i in range(self.n_channels):
            current_i = self.read_channel_current(i)
            chan_currents.append(i)

        return chan_currents

    def read_channel_current(self, channel_idx):
        assert channel_idx >= 0 and channel_idx < self.n_channels

        # Find which ADC of our adc_interfaces this channel belongs to
        adc_idx = channel_idx // CHANNELS_PER_ADC
        adc_subchannel_idx = adc_idx % CHANNELS_PER_ADC

        adc_interface = self.adc_interfaces[adc_idx]

        # @TODO move this into a separate getter field
        adc_interface.setGain(adc_interface.PGA_4_096V)

        # raw_ads_voltage = adc_interface.get_voltage(adc_subchannel_idx)
        raw_ads_val = adc_interface.readADC(adc_subchannel_idx)
        f = adc_interface.toVoltage()
        raw_ads_voltage = raw_ads_val * f

        # @TODO convert to voltage thru gain calculations
        print("voltage read: {}".format(raw_ads_voltage))

        # self.switch_i2cmultiplexer(module_idx)
        raise NotImplementedError()
    
    # Functions to set states
    
    """
    Sets all of the channel switches at the same time, to the new provided settings.
    This needs to be done all at once instead of manipulating channels individually, due to the way the switch shift
    register works.
    """
    def set_all_channel_switches(self, new_settings):
        if len(new_settings) != self.n_channels:
            raise Exception("set_all_channel_switches should be called with the new values for all of the channel switches")
        for setting in new_settings:
            if not isinstance(setting, bool):
                raise Exception("Invalid channel switch setting {}, should be True or False".format(setting))
        
        self.switch_shift_register.set_switches(new_settings)

        self.connected_channels = list(new_settings) # Update connected_channels to reflect new settings
        self._state_changed()

    
    """
    set_channel_voltage

    Sets the selected channel to the selected voltage
    """
    def set_channel_voltage(self, channel_idx: int, voltage: float):
        self.l.log("Setting channel {channel_idx} voltage to {v}".format(channel_idx=channel_idx, v=voltage))
        if channel_idx < 0 or channel_idx >= self.n_channels:
            raise Exception("Invalid channel idx {}. Must be 0 to {}".format(channel, self.n_channels - 1))

        dac_idx = channel_idx // CHANNELS_PER_ADC
        dac_subchannel_idx = channel_idx % CHANNELS_PER_DAC

        self.dac_interfaces[dac_idx].set_voltage(dac_subchannel_idx, voltage)
        self._state_changed()


    # """
    # switch_i2cmultiplexer

    # Uses the I2C multiplexer on the main board to select the given stack board,
    # so that the DACs and ADCs on that 8-channel board are available to the
    # Raspberry Pi
    # """
    # def switch_i2cmultiplexer(self, module_idx: int):
    #     if self.i2c_multiplexer.get_current_selected_module() == module_idx:
    #         return
    #     else:
    #         self.l.log("Switching I2C multiplexer to board {module_idx}".format(module_idx=module_idx))
    #         self.i2c_multiplexer.select_module(module_idx)

    """
    set_all_voltages

    Sets the all the voltages to the given list of voltages
    """
    def set_all_voltages(self, channel_voltages, suppress_state_change=False):
        assert len(channel_voltages) == self.n_channels
        # assert len(channel_indices) == len(channel_voltages)

        for chan_i in range(self.n_channels):
            chan_voltage = channel_voltages[i]

            self.set_channel_voltage(chan_i, chan_voltage, suppress_state_change=True)
            self.channel_voltages[chan_i] = chan_voltage
        
        if not suppress_state_change:
            self._state_changed()
    
    def reset_board():
        self.disconnect_all_electrodes(suppress_state_change=True)
        self.zero_all_voltages(suppress_state_change=True)

        #@TODO reset the settings of all the ADCs too
        # self.reset_all_
    


    def on_state_changed(self, listener):
        self.state_changed_listeners.append(listener)

    """
    This should be called when the Potentiostat class changes itself. Calling this notifies all listeners
    that data has changed
    """
    def _state_changed(self):
        for l in self.state_changed_listeners:
            l(self.get_state())

    
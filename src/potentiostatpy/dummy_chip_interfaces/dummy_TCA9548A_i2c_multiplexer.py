from ..logger import PrintLogger



class DummyTCA9548MultiplexerInterface:
    """
    This class manages the I2C multiplexer chip and performs tasks
    like changing the multiplexer's selected board.
    """
    def __init__(self, bus, n_modules: int, i2c_address: int, logger=PrintLogger()):
        self.bus = bus
        self.n_modules = n_modules
        self.i2c_address = i2c_address
        self.address = i2c_address
        self.l = logger
        self._current_module_selected = None

        self.l.log("Created multiplexer with n_modules {}".format(self.n_modules))
    
    def get_current_selected_module(self):
        return self._current_module_selected
    

    def select_module(self, module_idx):
        # Stop the user from pointing the device at a board that is not connected.
        assert module_idx in range(0, self.n_modules), "Expected module_idx {} to be in range(0, {})".format(module_idx, self.n_modules)
        if self._current_module_selected == module_idx:
            return
            
        # The command byte tells which modules to enable and disable I2C communication with
        # We only want to talk to one at a time, so we set all bits to zero except the one
        # corresponding to the module we want to talk to
        command_bytes = [
            0b00000001, # module 0
            0b00000010, # module 1
            0b00000100, # module 2
            0b00001000, # module 3
            0b00010000, # module 4
            0b00100000, # module 5
            0b01000000, # module 6
            0b10000000, # module 7
        ]

        com_byte = command_bytes[module_idx]
        self.l.log("Selecting module {module_idx} with TCA9548".format(module_idx=module_idx))
        self.l.log("Sending data 0x{:02x} to register 0x{:02x} at address 0x{:02x}".format(command_bytes[module_idx], 0x04, self.i2c_address))
        # self.bus.write_byte_data(self.i2c_address, 0x04, command_bytes[module_idx])
        self._current_module_selected = module_idx

class MCP4728Interface:
    def __init__(self, board_index, i2c_address):
        self.board_index = board_index
        self.i2c_address = i2c_address
    
    def reset():
        raise NotImplementedError()
    
    def set_voltage(channel, value):
        raise NotImplementedError()
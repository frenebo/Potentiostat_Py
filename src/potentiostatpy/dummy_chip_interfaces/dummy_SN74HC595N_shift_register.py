# import RPi.GPIO as GPIO
# import time

from ..logger import PrintLogger
# def hc595_



class DummySN74HC595NShiftRegister:
    """
    Simple class to switch the potentiostat's outputs on and off by controlling the switches with the linked shift registers.
    The different boards' shift registers are daisy-chained to each other, so we only need to send data to the first board, and the data
    will be shifted all the way to the last board eventually.
    """
    def __init__(self, SDI_pin, RCLK_pin, SRCLK_pin, num_channels, initialize=True, logger=PrintLogger()):
        self.SDI = SDI_pin
        self.RCLK = RCLK_pin
        self.SRCLK = SRCLK_pin
        self.l = logger
        
        assert num_channels % 8 == 0 # Each board contains eight channels, so num_channels should be a multiple of eight.
        self.num_channels = num_channels

        
        # if initialize:
        #     self.l.log("Initializing GPIO mode to GPIO.BOARD, setting pins to output mode")
        #     GPIO.setmode(GPIO.BOARD)
        #     GPIO.setup(self.SDI, GPIO.OUT)
        #     GPIO.setup(self.RCLK, GPIO.OUT)
        #     GPIO.setup(self.SRCLK, GPIO.OUT)
    
    def cleanup(self):
        self.l.log("Cleaning up GPIO pins with GPIO.cleanup()")
        # GPIO.cleanup()
            
    
    def set_switches(self, channel_states):
        self.l.log("Set switches called with channel_states {}".format(channel_states))
        pass
        # assert len(channel_states) == self.num_channels # Need to fill up the shift registers completely
        # for state in channel_states:
        #     assert isinstance(state, bool)
        
        # # Pin states at start
        # self.l.log("Setting switches to {}".format(channel_states))
        # self.l.log("    Setting SDI, RCKL, SRCLK outputs to low")
        # GPIO.output(self.SDI, GPIO.LOW)
        # GPIO.output(self.RCLK, GPIO.LOW)
        # GPIO.output(self.SRCLK, GPIO.LOW)

        # self.l.log("Loading channel states into the shift registers")
        # # We need to start with the last channel of the last board first, then work backwards - since the
        # # shift register shifts the bits down to the end by one every time we cycle the clock
        # for chan_state in reversed(channel_states):
        #     # Put the bit into the shift register, then input it and shift all the bits by one channel
        #     GPIO.output(self.SDI, chan_state)
        #     GPIO.output(self.SRCLK, GPIO.HIGH)
        #     time.sleep(0.0001)
        #     GPIO.output(self.SRCLK, GPIO.LOW)
        #     time.sleep(0.0001)
        
        # self.l.log("Latching RCLK to update the switch states from the new values in the shift registers")
        # # Once all data is loaded into the correct positions, we tell the shift registers to update their outputs to reflect
        # # their new data.
        # GPIO.output(self.RCLK, GPIO.HIGH)
        # time.sleep(0.0001)
        # GPIO.output(self.RCLK, GPIO.LOW)

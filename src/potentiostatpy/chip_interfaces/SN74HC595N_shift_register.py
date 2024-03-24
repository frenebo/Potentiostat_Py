import RPi.GPIO as GPIO
# def hc595_

# SDI -> pin 11 (gpio 17)
# RCLK  = pin 13 (gpio 27)
# SRCLK = pin 12 (gpio 18)


class SN75HC595NShiftRegister:
    def __init__(self, DS_pin, RCLK_pin, SRCLK_pin, num_channels, initialize=True):
        self.DS = SPI_pin
        self.RCLK = RCLK_pin
        self.SRCLK = SRCLK_pin
        
        assert num_channels % 8 == 0 # Each board contains eight channels, so num_channels should be a multiple of eight.
        self.num_channels = num_channels

        # self.switch_states = 
        
        if initialize:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(SDI, GPIO.OUT)
            GPIO.setup(RCLK, GPIO.OUT)
            GPIO.setup(SRCLK, GPIO.OUT)
            
    
    def set_switches(self, channel_states):
        assert len(channel_states) == self.num_channels # Need to fill up the shift registers completely
        # Pin states at start
        GPIO.output(SDI, GPIO.LOW)
        GPIO.output(RCLK, GPIO.LOW)
        GPIO.output(SRCLK, GPIO.LOW)

        # We need to start with the last channel of the last board first, then work backwards - since the
        # shift register shifts the bits down to the end by one every time we cycle the clock
        for chan_state in reversed(channel_states):
            # Put the bit into the shift register, then input it and shift all the bits by one channel
            GPIO.output(SDI, chan_state)
            GPIO.output(SRCLK, GPIO.HIGH)
            time.sleep(0.0001)
            GPIO.output(SRCLK, GPIO.LOW)
            time.sleep(0.0001)
        
        # Once all data is loaded into the correct positions, we tell the shift registers to update their outputs to reflect
        # their new data.
        GPIO.output(RCLK, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(RCLK, GPIO.LOW)

# #Shift data out
# def hc595_in(dat):
#     for bit in range(0, 8):
#         #print(0x80 & dat<<bit)
# 	GPIO.output(SDI, 0x80 & (dat << bit))
# 	GPIO.output(SRCLK, GPIO.HIGH)
# 	time.sleep(0.01)
# 	GPIO.output(SRCLK, GPIO.LOW)
# 	time.sleep(0.01)

    
# #Toggle CLK
# def hc595_out():
#     GPIO.output(RCLK, GPIO.HIGH)
#     time.sleep(0.001)
#     GPIO.output(RCLK, GPIO.LOW)

# #Latch shift register outputs
# def hc595_update():
#     for i in range(number_expansion_board-1,-1,-1):
#         hc595_in(switch_data[i])
#         print(i,str(bin(switch_data[i])))
#         time.sleep(0.01)
#     time.sleep(0.01)
#     hc595_out()

#     def zero_out_pins
    

#     # GPIO.setup(SDI, GPIO.OUT)
#     # GPIO.setup(RCLK, GPIO.OUT)
#     # GPIO.setup(SRCLK, GPIO.OUT)
#     # GPIO.output(SDI, GPIO.LOW)
#     # GPIO.output(RCLK, GPIO.LOW)
#     # GPIO.output(SRCLK, GPIO.LOW)
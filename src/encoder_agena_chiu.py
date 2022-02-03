'''!
@file encoder_agena_chiu.py
This is the file that serves as a module to be imported in main. It creates a class for the encoder driver
to run functions.
@author Corey Agena
@author Luisa Chiu
@date 1-26-2022
'''
import pyb

class EncoderDriver:  
    '''! 
    This class implements a encoder driver for an ME405 kit. 
    '''
    def __init__(self, in1pin, in2pin, timer):
        '''! 
        Creates a encoder driver by initializing encoder
        pins. 
        @param in1pin Pin 1 to read the encoder.
        @param in2pin Pin 2 to read the encoder.
        @param timer Timer to use for encoder channels.
        '''
        
        ## The timer variable for the motor.
        self.tim = pyb.Timer(timer, prescaler = 0, period = 65535)
        
        ## A pin variable to recieve the duty cycles.
        self.pin1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        ## A pin variable to recieve the duty cycles.
        self.pin2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        
        ## The channel variable for channel 1 and pin1.
        self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB,
                                    pin = self.pin1)
        ## The channel variable for channel 2 and pin2.
        self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB,
                                    pin = self.pin2)
        
        ## The initial position is set to zero.
        self.pos = 0
        
        ## The initial past time is set to zero.
        self.past = 0
    
    def read(self):
        '''!
        Reads the encoder position and returns the values.
        @return The position of the encoder.
        '''
        ## The variable that marks the start of the timer.
        self.current = self.tim.counter()
        ## The variable that calculates change in time.
        self.delta = self.current - self.past
        if self.delta < -32768:
            self.delta += 65536
        elif self.delta > 32768:
            self.delta -= 65536
        self.pos += self.delta
        self.past = self.current
        return self.pos

    def zero(self):
        '''!
        Sets the encoder reading to zero.
        '''
        self.pos = 0   
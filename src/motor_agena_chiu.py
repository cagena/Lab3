'''!
@file motor_agena_chiu.py
This is the file that serves as a module to be imported in main. It creates a class for the motor driver
to run functions.
@author Corey Agena
@author Luisa Chiu
@date 1-26-2022
'''

import pyb
    
class MotorDriver:  
    '''! 
    This class implements a motor driver for an ME405 kit. 
    '''
    def __init__(self, en_pin, in1pin, in2pin, timer):
        '''! 
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. 
        @param en_pin pin for enabling the motor.
        @param in1pin pin 1 to control the motor.
        @param in2pin pin 2 to control the motor.
        @param timer timer to use for motor channels.
        '''
        ## The pin variable for the enable pin on the Nucleo.
        self.EN = pyb.Pin(en_pin, mode = pyb.Pin.OUT_OD,
                          pull = pyb.Pin.PULL_UP)
        
        ## The timer variable for the motor.
        self.tim = pyb.Timer(timer, freq = 20000)
        
        ## A pin variable to recieve the duty cycles.
        self.pin1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        ## A pin variable to recieve the duty cycles.
        self.pin2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        
        ## The channel variable for channel 1 and pin1.
        self.ch1 = self.tim.channel(1, mode = pyb.Timer.PWM,
                                    pin = self.pin1)
        ## The channel variable for channel 2 and pin2.
        self.ch2 = self.tim.channel(2, mode = pyb.Timer.PWM,
                                    pin = self.pin2)
        
        # Turn the motor off for safety.
        self.pin1.low()
        self.pin2.low()
        
        print ('Creating a motor driver')
        
    def enable(self):
        '''!
        Enables the motor, allowing power to it.
        '''
        self.EN.high()
        
    def disable(self):
        '''!
        Disables the motor, preventing power to it.
        '''
        self.EN.low()
        
    def set_duty_cycle(self, duty):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param duty A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        if duty > 0:
            self.ch1.pulse_width_percent(duty)
            self.ch2.pulse_width_percent(0)
        elif duty < 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(-duty)  
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0) 
            
#        print ('Setting duty cycle to ' + str (duty))   
'''!
@file controller_agena_chiu.py
This is the file that serves as a module to be imported in main. It creates a class for the controller
driver to run functions.
@author Corey Agena
@author Luisa Chiu
@date 1-27-2022
'''

import pyb
    
class ControllerDriver:  
    '''! 
    This class implements a controller driver for a motor and flywheel rig. 
    '''
    def __init__(self, K_p, i_set):
        '''! 
        Creates a controller driver by initializing the gain
        and initial setpoint used in closed-loop control.
        @param K_p The initial proportional gain for the controller.
        @param i_set The initial setpoint for the controller.
        '''
        ## Proportional Gain
        self.K_p = float(K_p)
        
        ## Initial setpoint
        self.i_set = float(i_set)
        
    def run(self,pos):
        '''!
        Called repeatedly to run the control algorithm.
        @param pos Current position of the encoder.
        @return duty Duty cycle to set the motor.
        '''
        ## Error, difference between the current position and initial setpoint.
        if pos < self.i_set:
            error = abs(pos - self.i_set)
        elif pos > self.i_set:
            error = abs(pos - self.i_set)*(-1)
        ## Actuation signal or percent duty cycle to set the motor.
        duty = error*self.K_p
        if duty > 100:
            duty = 100
        elif duty < -100:
            duty = -100
        return duty
        
    def set_setpoint(self,setpoint):
        '''!
        Sets the setpoint.
        @param setpoint The new setpoint used for the controller.
        '''
        self.i_set = float(setpoint)
        
    def set_gain(self, gain):
        '''!
        Sets the proportional gain.
        @param gain The new proportional gain used for the controller.
        '''
        self.K_p = float(gain)
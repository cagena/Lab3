"""!
@file main.py
This is the main file for Lab 3, it contains a program that runs two motor tasks which includes closed loop control
for each motor. The code was adapted from Dr. Ridgely's basic task example.
@author Corey Agena
@author Luisa Chiu
@date 2-9-2022
"""

import gc
import pyb
import cotask
import encoder_agena_chiu
import motor_agena_chiu
import controller_agena_chiu
import utime
import print_task

def task_motor1():
    ## The variable that calculates change in time.
    difference = 0
    ## The variable that marks the start of the timer.
    start = utime.ticks_ms()
    ## The variable that indicates if the current run is the initial run of the loop.
    runs1 = 0
    while True:
        ## A variable that creates a timer which marks the current time.
        current = utime.ticks_ms()
        difference = (current - start)
        ## A variable that defines duty cycle for the controller's run function.
        duty_cycle = controller_1.run(encoder_drv1.read())
        motor_drv1.set_duty_cycle(duty_cycle)

        if difference <= 1500:
            print_task.put('{:},{:}\r\n'.format(difference,encoder_drv1.read()))
        else:
            if runs1 == 0:
                print_task.put('Done\r\n')
                motor_drv1.disable()
                runs1 = 1
        yield()

def task_motor2():
    ## The variable that calculates change in time.
    difference = 0
    ## The variable that marks the start of the timer.
    start = utime.ticks_ms()
    while True:
        ## A variable that creates a timer which marks the current time.
        current = utime.ticks_ms()
        difference = (current - start)
        ## A variable that defines duty cycle for the controller's run function.
        duty_cycle = controller_2.run(encoder_drv2.read())
        motor_drv2.set_duty_cycle(duty_cycle)
        if difference >= 1500:
            motor_drv2.disable()
        # The print portion is commented out for the second motor.
            # if difference <= 1500:
            # print_task.put('{:},{:}\r\n'.format(difference,encoder_drv2.read()))
        yield()

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    ## A variable that creates a encoder driver for encoder 1.
    encoder_drv1 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    ## A variable that creates a encoder driver for encoder 2.
    encoder_drv2 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    ## A variable that creates a motor driver for motor 1.
    motor_drv1 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    ## A variable that creates a motor driver for motor 2.
    motor_drv2 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    ## A variable that creates a controller driver for motor 1.
    controller_1 = controller_agena_chiu.ControllerDriver(0, 0)
    ## A variable that creates a controller driver for motor 2.
    controller_2 = controller_agena_chiu.ControllerDriver(0, 0)
    # Enable both motors.
    motor_drv1.enable()
    motor_drv2.enable()

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    x = input('Input Kp to run step response, input s to stop: ')
    try:
        float(x)
    except:
        if x == 's':
            motor_drv1.set_duty_cycle(0)
            motor_drv2.set_duty_cycle(0)
    else:
        ## A variable that requests for set point from the user.
        y = input('Input set point: ')
        controller_1.set_gain(x)
        controller_1.set_setpoint(y)
        controller_2.set_gain(x)
        controller_2.set_setpoint(y)
        encoder_drv1.zero()
        encoder_drv2.zero()
        # Create the tasks. If trace is enabled for any task, memory will be
        # allocated for state transition tracing, and the application will run out
        # of memory after a while and quit. Therefore, use tracing only for 
        # debugging and set trace to False when it's not needed
        task1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 1, 
                             period = 10, profile = True, trace = False)
        task2 = cotask.Task (task_motor2, name = 'Task_Motor2', priority = 1, 
                             period = 10, profile = True, trace = False)
        cotask.task_list.append (task1)
        cotask.task_list.append (task2)
        while True:
            # Run the scheduler with the chosen scheduling algorithm. 
            cotask.task_list.pri_sched ()
    
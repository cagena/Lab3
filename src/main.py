"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import encoder_agena_chiu
import motor_agena_chiu
import controller_agena_chiu
import utime
import print_task
# def task1_fun ():
#     """!
#     Task which puts things into a share and a queue.
#     """
#     counter = 0
#     while True:
#         share0.put (counter)
#         q0.put (counter)
#         counter += 1

#         yield (0)


def task_motor1():
    start = utime.ticks_ms()
    while True:
        ## A variable that creates a timer which marks the current time.
        current = utime.ticks_ms()
        difference = current - start
        ## A variable that defines duty cycle for the controller's run function.
        duty_cycle = controller.run(encoder_drv1.read())
        motor_drv1.set_duty_cycle(duty_cycle)
#         time1.put(difference)
#         enc_pos1.put(encoder_drv1.read())
        print_task.put('{:},{:}\r\n'.format(difference,encoder_drv1.read()))
        if difference >= 1500:
            break
        yield()

def task2_fun ():
    """!
    Task which takes things out of a queue and share to display.
    """
    while True:
        # Show everything currently in the queue and the value in the share
        print ("Share: {:}, Queue: ".format (share0.get ()), end='');
        while q0.any ():
            print ("{:} ".format (q0.get ()), end='')
        print ('')

        yield (0)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    ## A variable that creates a encoder driver for encoder 1.
    encoder_drv1 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    # A variable that creates a encoder driver for encoder 2.
    # encoder_drv2 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    ## A variable that creates a motor driver for motor 1.
    motor_drv1 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    # A variable that creates a motor driver for motor 2.
    # motor_drv2 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    ## A variable that creates a controller driver.
    controller = controller_agena_chiu.ControllerDriver(0, 0)
    # Enable both motors.
    motor_drv1.enable()
    # motor_drv2.enable()
    # Set the duty cycle for both motors.
    
    ## A variable that requests for proportional gain from the user.
#     x1 = input('Input Kp to run step response, input s to stop: ')
#     try:
#         float(x1)
#     except:
#         if x == 's':
#             motor_drv1.set_duty_cycle(0)
#     else:
#         ## A variable that requests for set point from the user.
#         y1 = input('Input set point: ')
#         controller.set_gain(x1)
#         controller.set_setpoint(y1)
#         encoder_drv1.zero()
    controller.set_gain(0.1)
    controller.set_setpoint(16384)
    encoder_drv1.zero()
            
#     ## A variable that requests for proportional gain from the user.
#     Kp_motor1 = task_share.Share ('h', thread_protect = False, name = "Kp1 Share")
#     x1 = input('Input Kp to run step response, input s to stop: ')
#     Kp_motor1.put(x1)
#     
#     ## A variable that requests for set point from the user.
#     setpt_motor1 = task_share.Share ('l', thread_protect = False, name = "Set Point Share")
#     y1 = input('Input set point: ')
#     setpt_motor1.put(y1)
    
#     controller.set_gain(Kp_motor1.get())
#     controller.set_setpoint(setpt_motor1.get())
#     encoder_drv1.zero()
    
    ## A variable that marks the start of the timer.
    start_time = task_share.Share ('l', thread_protect = False, name = "Start Time Share")
    ## A variable that creates an empty list to be populated with time data.
#     time1 = task_share.Queue ('l', 16, thread_protect = False, overwrite = False,
#                            name = "Time Q 1")
#     ## A variable that creates an empty list to be populated with encoder position data.
#     enc_pos1 = task_share.Queue ('l', 16, thread_protect = False, overwrite = False,
#                            name = "Encoder Position Q 1")
    
#     print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
#            'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
#     share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
#     q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
#                            name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 1, 
                         period = 10, profile = True, trace = False)
    #task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
    #                     period = 1500, profile = True, trace = False)
    cotask.task_list.append (task1)
    #cotask.task_list.append (task2)
    
#     task2 = cotask.Task (task_motor1, name = 'Printing', priority = 0)
#     cotask.task_list.append (task2) 

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    start_time.put(utime.ticks_ms())
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    
#     motor_drv1.set_duty_cycle(0)
#     print('{:},{:}'.format(time1.get(),enc_pos1.get()))

    # Print a table of task data and a table of shared information data
#     print ('\n' + str (cotask.task_list))
#     print (task_share.show_all ())
#     print (task1.get_trace ())
#     print ('\r\n')

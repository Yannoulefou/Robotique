import sys
import time

from telemetrix import telemetrix


# flag to keep track of the number of times the callback
# was called. When == 2, exit program
exit_flag = 0


def the_callback(data):
    global exit_flag
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
    print(f'Motor {data[1]} absolute motion completed at: {date}.')
    exit_flag += 1


def running_callback(data):
    if data[1]:
        print('The motor is running.')
    else:
        print('The motor IS NOT running.')


def step_absolute(the_board):
    global exit_flag
    motor = the_board.set_pin_mode_stepper(interface=4, pin1=8, pin2=9, pin3=10, pin4=11)
    time.sleep(.5)

    # set the max speed and acceleration
    the_board.stepper_set_current_position(0, 0)
    the_board.stepper_set_max_speed(motor, 400)
    the_board.stepper_set_acceleration(motor, 800)



    # keep application running
    while True:
        try:
            # set the absolute position in steps
            the_board.stepper_move_to(motor, int(input('Enter a position in steps: ')))

            # run the motor
            print('Starting motor...')
            the_board.stepper_run(motor, completion_callback=the_callback)
            time.sleep(.2)
            the_board.stepper_is_running(motor, callback=running_callback)
            time.sleep(.2)
        except KeyboardInterrupt:
            the_board.shutdown()
            sys.exit(0)
    the_board.shutdown()
    sys.exit(0)


# instantiate telemetrix
board = telemetrix.Telemetrix()
try:
    # start the main function
    step_absolute(board)
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
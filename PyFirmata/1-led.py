import pyfirmata, time

board = pyfirmata.Arduino("/dev/ttyACM0")
it = pyfirmata.util.Iterator(board)
it.start()
led = board.get_pin("d:11:o")
while True:
    time.sleep(1)
    print("High")
    board.digital[11].write(1)
    time.sleep(1)
    print("Low")
    board.digital[11].write(0)



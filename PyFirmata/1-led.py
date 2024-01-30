import pyfirmata, time

board = pyfirmata.Arduino("COM3")
it = pyfirmata.util.Iterator(board)
it.start()
led = board.get_pin("d:11:o")
led = board.get_pin("d:10:o")
while True:
    time.sleep(1)
    print("High")
    board.digital[11].write(1)
    board.digital[10].write(0)
    time.sleep(1)
    print("Low")
    board.digital[11].write(0)
    board.digital[10].write(1)



import pyfirmata, time


pin1 = 8
pin2 = 9
pin3 = 10
pin4 = 11

board = pyfirmata.Arduino("COM3")
it = pyfirmata.util.Iterator(board)
it.start()

def motor_step(liste_pins, liste_open):
    for i in range(4):
        board.digital[liste_pins[i]].write(0)
    for j in liste_open:
        board.digital[liste_pins[j]].write(1)


while True:
    for liste_open in [[0], [0, 2], [2], [2, 1], [1], [1, 3], [3], [3, 0]]:
        motor_step([pin1, pin2, pin3, pin4], liste_open)
        time.sleep(0.0001)

import serial
import time
import math
"""
# Configuration du port série
ser = serial.Serial('COM4', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 0.1  # Définir le délai de lecture du port série
"""
def lecture_gyro():
    # Lire une ligne de données sérialisées depuis Arduino
    line = ser.readline().decode()
    values = line.split(',')
    # Assurer qu'il y a six valeurs dans la ligne
    if len(values) == 6:
        # Convertir chaque valeur en float
        try:
            ax = float(values[0])
            ay = float(values[1])
            az = float(values[2])
            gx = float(values[3])
            gy = float(values[4])
            gz = float(values[5])
            # Afficher les valeurs converties
            #print("ax:", ax, "ay:", ay, "az:", az, "gx:", gx, "gy:", gy, "gz:", gz)
            time.sleep(0.1)
            return ax, ay, az, gx, gy, gz
        except ValueError:
            print("Erreur de conversion en float")
    else:
        print("Erreur: la ligne ne contient pas 6 valeurs")

# Fonction pour calculer la position et la direction du robot avec les données du gyroscope
def calculer_position(x_prec, y_prec, angle_prec, ax, ay, az, gx, gy, gz, dt=1):
    x_gyro = 0.5*ax*1000*(dt**2)     # calculer la valeur de x dans le repère du gyroscope (on passe en mm)
    y_gyro = 0.5*ay*1000*(dt**2)     # calculer la valeur de y dans le repère du gyroscope (on passe en mm)
    print("y_gyro = ", y_gyro)
    rotation = gz*dt     # calculer la rotation du robot en radians
    print("rotation = ", rotation)
    new_angle = angle_prec + rotation    # calculer la direction robot dans le repère global
    print("new_angle =", new_angle)
    new_x = x_prec + (x_gyro*math.cos(rotation) - y_gyro*math.sin(rotation))   # calculer la valeur de x dans le repère global
    new_y = y_prec + (x_gyro*math.sin(rotation) + y_gyro*math.cos(rotation))   # calculer la valeur de y dans le repère global
    print(new_x, new_y, new_angle)
    return new_x, new_y, new_angle
    

x_prec = 0
y_prec = 0
angle_prec = math.pi/2

for i in range(10) :
    x_prec, y_prec, angle_prec = calculer_position(x_prec, y_prec, angle_prec, 1, 1, 0, 0, 0, 0)

""" 
time.sleep(10)
while True:
    time.sleep(0.1)
    #print(lecture_gyro())
    ax, ay, az, gx, gy, gz = lecture_gyro()
    print(calculer_position(x_prec, y_prec, angle_prec, ax, ay, az, gx, gy, gz))
"""
import serial
import time
import math

# Configuration du port série
ser = serial.Serial('COM4', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 1  # Définir le délai de lecture du port série

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
            return (ax, ay, az, gx, gy, gz)
        except ValueError:
            print("Erreur de conversion en float")
    else:
        print("Erreur: la ligne ne contient pas 6 valeurs")
    
time.sleep(10)
while True:
    time.sleep(0.001)
    print(lecture_gyro())
    ax, ay, az, gx, gy, gz = lecture_gyro()
    x_prec = 0
    y_prec = 0
    angle_prec = math.pi/2

    # Fonction pour calculer la position du robot avec les données du gyroscope
    def calculer_position(x_prec, y_prec, angle_prec, ax, ay, az, gx, gy, gz, dt=0.01):
        x_gyro = ax*1000*(dt**2)     # calculer la valeur de x dans le repère du gyroscope (on passe en mm)
        y_gyro = ay*1000*(dt**2)     # calculer la valeur de y dans le repère du gyroscope (on passe en mm)
        alpha = 0.49        # facteur d'interpolation, qui donne plus de poids au gyroscope qu'à l'accéléromètre
        angle_gyro = alpha*(math.pi/2+gx*dt) + alpha*(math.pi/2+gy*dt) + (1-2*alpha)*(math.atan(y_gyro/x_gyro))        # calculer l'angle du robot dans le repère du gyroscope par une moyenne pondérée des différentes méthodes possibles
        distance = (x_gyro**2 + y_gyro**2)**0.5  # calculer la distance parcourue par le robot
        angle = round(angle_prec + angle_gyro - (math.pi/2), 2)     # calculer l'angle du robot dans le repère global
        new_x = round(x_prec + distance * math.cos(angle))       # calculer la valeur de x dans le repère global
        new_y = round(y_prec + distance * math.sin(angle))       # calculer la valeur de y dans le repère global
        return new_x, new_y, angle

    print(calculer_position(x_prec, y_prec, angle_prec, ax, ay, az, gx, gy, gz))
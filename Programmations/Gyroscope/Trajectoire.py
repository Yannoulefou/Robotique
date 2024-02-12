import serial
import time
import math


# Configuration du port série
ser = serial.Serial('COM4', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 0.1  # Définir le délai de lecture du port série

def lire_gyro():
    # Lire une ligne de données sérialisées depuis Arduino
    line = ser.readline().decode().strip()

    # Diviser la ligne en valeurs individuelles
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
            print("ax:", ax, "ay:", ay, "az:", az, "gx:", gx, "gy:", gy, "gz:", gz)
        except ValueError:
            print("Erreur de conversion en float")
    else:
        print("Erreur: la ligne ne contient pas 6 valeurs")
    time.sleep(0.1)
    return ax, ay, az, gx, gy, gz



# Fonction pour calculer la position du robot avec les données du gyroscope
def calculer_position(x_prec, y_prec, angle_prec, ax, ay, az, gx, gy, gz, dt=0.01):
    x_gyro = ax*1000*(dt**2)     # calculer la valeur de x dans le repère du gyroscope (on passe en mm)
    y_gyro = ay*1000*(dt**2)     # calculer la valeur de y dans le repère du gyroscope (on passe en mm)
    alpha = 0.49        # facteur d'interpolation, qui donne plus de poids au gyroscope qu'à l'accéléromètre
    angle_gyro = alpha*(math.pi/2+gx*dt) + alpha*(math.pi/2+gy*dt) + (1-2*alpha)*(math.atan(y_gyro/x_gyro))        # calculer l'angle du robot dans le repère du gyroscope par une moyenne pondérée des différentes méthodes possibles
    distance = (x_gyro**2 + y_gyro**2)**0.5  # calculer la distance parcourue par le robot
    new_angle = round(angle_prec + angle_gyro - (math.pi/2), 2)     # calculer l'angle du robot dans le repère global
    new_x = round(x_prec + distance * math.cos(angle))       # calculer la valeur de x dans le repère global
    new_y = round(y_prec + distance * math.sin(angle))       # calculer la valeur de y dans le repère global
    return new_x, new_y, new_angle


# Fonction qui met à jour la position du robot au fil du temps dans le repère global avec les données du gyroscope
def start_position() :
    x, y, angle = 0, 0, math.pi/2

    # Démarrage de la mise à jour de la position du robot dans un thread séparé
    import threading
    update_thread = threading.Thread(target=update_position, args=(x, y, angle))
    update_thread.start()

def update_position(x,y,angle) : 
    while True :
        x, y, angle = calculer_position(x, y, angle, lire_gyro())
        time.sleep(1)

# Obtention de la position actuelle du robot
def obtenir_position():
    global x, y, angle
    return x, y, angle


# Fonction qui calcule un angle au cours d'une rotation (et pas un angle par rapport au repère global)
def calculer_angle(gx, dt) :
        angle = 0
        while gx > 0.1 : # tant que le robot tourne, on incrémente la valeur de l'angle
            angle+= gx*dt
            time.sleep(dt)
            gx = lecture_gyro[3]
        return angle

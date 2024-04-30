"""Il est probable que la fonction de calcul de la position ne soit pas utile car codée sous Arduino."""

import serial
import time
import math


# Configuration du port série
ser = serial.Serial('COM5', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 0.1  # Définir le délai de lecture du port série

def lire_gyro():
    # Lire une ligne de données sérialisées depuis Arduino par le programme gyroscope_valeurs_corrigees
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



def calculer_position(x_prec, y_prec, angle_prec, ax, ay, az, gx, gy, gz, vx_prec, vy_prec, dt=1):
    """ Fonction qui calcule la position et la direction du robot avec les données du gyroscope
        Même programme que "gyroscope_calcul_position" écrit en C++. """
    vx = 0.5*(ax*dt + vx_prec)
    vy = 0.5*(ay*dt + vy_prec)
    x_gyro = vx*dt*1000    # calculer la valeur de x dans le repère du gyroscope (on passe en mm)
    y_gyro = vy*dt*1000    # calculer la valeur de y dans le repère du gyroscope (on passe en mm)
    rotation = gz*dt     # calculer la rotation du robot en radians
    new_angle = angle_prec + rotation    # calculer la direction robot dans le repère global
    new_x = x_prec + (x_gyro*math.cos(new_angle) - y_gyro*math.sin(new_angle))   # calculer la valeur de x dans le repère global
    new_y = y_prec + (x_gyro*math.sin(new_angle) + y_gyro*math.cos(new_angle))   # calculer la valeur de y dans le repère global
    return new_x, new_y, new_angle



def obtenir_position():
    while True:
        # Lire une ligne de données sérialisées depuis Arduino par le programme gyroscope_calcul_position
        line = ser.readline().decode().strip()

        # Diviser la ligne en valeurs individuelles
        values = line.split(',')

        # Assurer qu'il y a trois valeurs dans la ligne
        if len(values) == 3 :
            if len(values[0].split()) == 4 and len(values[1].split()) == 4 and len(values[2].split()) == 3 :
                # Convertir chaque valeur en float
                x = float(values[0].split()[2])
                y = float(values[1].split()[2])
                angle = float(values[2].split()[1])
                return x, y, angle  # Retourner les valeurs si tout est lu correctement
            else : # Si la ligne n'a pas le format attendu, passer à la prochaine ligne
                continue
        else:
            # Si la ligne n'a pas les trois valeurs attendues, passer à la prochaine ligne
            continue


# Fonction qui calcule un angle au cours d'une rotation (et pas un angle par rapport au repère global)
rotation = None
def calculer_rotation(gz, dt) :
    global rotation 
    rotation = 0
    while abs(gz)>0.1 : # tant que le robot tourne, on incrémente la valeur de l'angle
        gz = lire_gyro()[5]
        rotation+= gz*dt    # Stocker la valeur finale de l'angle dans une variable globale
        time.sleep(dt)

ser.close() # Fermer le port série
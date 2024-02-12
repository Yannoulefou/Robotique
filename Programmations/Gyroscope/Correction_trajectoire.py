import serial
from BaseDiff import BaseDiff, BaseDiffCalcul
import time
import math

# Simulation ou connecté à une Arduino
is_simulation = False

if is_simulation:
    base_diff = BaseDiffCalcul(x=225, y=225, angle=0)
else:
    import sys
    import time

    from telemetrix import telemetrix

    board = telemetrix.Telemetrix()
    base_diff = BaseDiff(board=board, x=225, y=225, angle=0, pinsG=[4, 5, 6, 7], pinsD=[8, 9, 10, 11]   )


# Configuration du port série
ser = serial.Serial('COM4', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 1  # Définir le délai de lecture du port série

def lecture_gyro():
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

lecture_gyro()


# Fonction pour calculer la position du robot avec les données du gyroscope
def calculer_position(angle_prec, x_prec, y_prec, ax, ay, az, gx, gy, gz, dt=0.01):
    dx = ax*(dt**2)     # calculer la valeur de x dans le repère du gyroscope
    dy = ay*(dt**2)     # calculer la valeur de y dans le repère du gyroscope
    alpha = 0.49        # facteur d'interpolation, qui donne plus de poids au gyroscope qu'à l'accéléromètre
    rotation = alpha*gx*dt + alpha*((math.pi/2)*gy*dt) + (1-2*alpha)*(math.atan(dy/dx))        # calculer la rotation du robot dans le repère du gyroscope par une moyenne pondérée des différentes méthodes possibles
    distance = 0.5*(dx/math.cos(math.radians(rotation))) + 0.5*(dy/math.sin(math.radians(rotation))) # calculer la distance parcourue par le robot
    angle = angle_prec + rotation - (math.pi/2)     # calculer l'angle du robot dans le repère global
    x = x_prec + distance * math.cos(math.radians(angle))       # calculer la valeur de x dans le repère global
    y = y_prec + distance * math.sin(math.radians(angle))       # calculer la valeur de y dans le repère global
    return x, y, angle


v = 600
liste_actions = [ # Liste des actions à effectuer dans un couple (fonctions, arguments)
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 200, 'pasD': 0 }), # 45 °
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 700, 'pasD': 700}), # Avancer tout droit (env. 1096mm diviser par 0.31)
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -550, 'pasD': 550}), # Demi tour
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 500, 'pasD': 500 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -600, 'pasD': -600 }), # Reculer tout droit
     (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -400, 'pasD': 400}), # Tourner 
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 600, 'pasD': 600 }), # Avancer tout droit
     (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 250, 'pasD': -250}), # Tourner 
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 600, 'pasD': 600 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -1200, 'pasD': -1200 }), # Reculer tout droit
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -550, 'pasD': 550}), # Demi tour
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 700, 'pasD': 700 }), # Avancer tout droit
]


# Parcourir la liste des actions
for action, arguments in liste_actions:
    action(**arguments)  # Appeler la fonction avec les arguments fournis
    # Après chaque action, ajuster la position en fonction de celle observée par le gyroscope
    ax, ay, az, gx, gy, gz = lecture_gyro()
    angle_gyro = calculer_angle_rotation(ax, ay, az, gx, gy, gz)
    position_gyro = calculer_position(angle_gyro, x_prev, y_prev)
    base_diff.ajuster_position(v, v, position_gyro)
    time.sleep(0.5)  # Attente pour éviter d'envoyer des commandes trop rapidement
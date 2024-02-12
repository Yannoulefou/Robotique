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

# Fonction pour calculer l'angle de rotation en degrés
def calculer_angle_rotation(ax, ay, az, gx, gy, gz):
    # Convertir les valeurs d'accélération en angles
    angle_acc = math.atan2(ay, az)

    # Calculer l'angle de rotation en fonction des valeurs du gyroscope
    dt = 0.01  # Temps écoulé depuis la dernière lecture (en secondes)
    angle_gyro = (gx * dt)  # En supposant que la vitesse angulaire est constante sur une petite période

    # Combiner les deux angles en prenant une moyenne pondérée
    alpha = 0.98  # Facteur d'interpolation
    angle = alpha * (angle_gyro) + (1 - alpha) * (angle_acc)

    return angle

# Fonction pour calculer la position du robot en fonction de l'angle de rotation autour des axes x et y
def calculer_position(angle, x_prev, y_prev):
    # Supposons que le robot se déplace uniquement selon l'axe x
    distance = 0.1  # Distance parcourue depuis la dernière lecture (en mètres)
    x = x_prev + distance * math.cos(math.radians(angle))
    y = y_prev + distance * math.sin(math.radians(angle))
    return x, y


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
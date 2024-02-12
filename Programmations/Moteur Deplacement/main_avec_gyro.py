import serial
from BaseDiff import BaseDiff, BaseDiffCalcul
import time
from Gyroscope.Trajectoire import lire_gyro, calculer_angle
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



dt = 0.01
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
    if float(arguments['pasG']) < 0 or float(arguments['pasD']) < 0 :     # Si le robot doit effectuer une rotation, on utilise le gyroscope pour mesurer l'angle réaliser et éventuellement l'ajuster
        action(**arguments)                                               # Appeler la fonction avec les arguments fournis
        angle_réel = calculer_angle(lire_gyro[3])
        base_diff.ajuster_angle(v, v, float(arguments['pasG']), float(arguments['pasD']), angle_réel)

    else :
        action(**arguments)  # Appeler la fonction avec les arguments fournis
        # position_gyro = calculer_position(angle_gyro, x_prev, y_prev)
        # base_diff.ajuster_position(v, v, position_gyro)
    time.sleep(0.5)  # Attente pour éviter d'envoyer des commandes trop rapidement
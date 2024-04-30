import serial
from BaseDiff import BaseDiff, BaseDiffCalcul
import time
from Trajectoire import lire_gyro, calculer_rotation, obtenir_position
import threading

# Simulation ou connecté à une Arduino
is_simulation = True

if is_simulation:
    base_diff = BaseDiffCalcul(x=225, y=225, angle=0)
else:
    import sys
    import time

    from telemetrix import telemetrix

    board = telemetrix.Telemetrix()
    base_diff = BaseDiff(board=board, x=225, y=225, angle=0, pinsG=[4, 5, 6, 7], pinsD=[8, 9, 10, 11]   )


# Configuration du port série
ser = serial.Serial('COM5', 115200)  # Remplacez 'COM4' par le port série approprié
ser.timeout = 0.1  # Définir le délai de lecture du port série

dt = 0.1
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


# Fonction qui calcule un angle au cours d'une rotation (et pas un angle par rapport au repère global)
rotation = None
def calculer_rotation(gz, dt) :
    global rotation 
    rotation = 0
    while abs(gz)>0.1 : # tant que le robot tourne, on incrémente la valeur de l'angle
        gz = lire_gyro()[5]
        rotation+= gz*dt    # Stocker la valeur finale de l'angle dans une variable globale
        time.sleep(dt)


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
        print("Erreur: la ligne ne contient pas 6 valeurs :", values)
    time.sleep(0.1)
    return ax, ay, az, gx, gy, gz


# Parcourir la liste des actions
for action, arguments in liste_actions:
    if float(arguments['pasG']) < 0 or float(arguments['pasD']) < 0 :     # Si le robot doit effectuer une rotation, on utilise le gyroscope pour mesurer l'angle réalisé et éventuellement l'ajuster

        # Créer le thread pour calculer la rotation et le démarrer
        thread_rotation = threading.Thread(target=calculer_rotation, args=(lire_gyro()[5], 0.1))
        thread_rotation.start()

        # Créer le thread pour tourner les roues et le démarrer
        thread_tourner_roues = threading.Thread(target=action, args=(arguments,))
        thread_tourner_roues.start()

        # Attendre que le thread de tourner_roues se termine
        thread_tourner_roues.join()

        # Ajuster la rotation des roues à partir de l'erreur détectée par le gyroscope
        base_diff.ajuster_angle(v, v, float(arguments['pasG']), float(arguments['pasD']), rotation)

    else :
        action(**arguments)  # Appeler la fonction avec les arguments fournis
        # position_gyro = obtenir_position()  # position_gyro = (x, y, angle)
        # base_diff.ajuster_position(v, v, position_gyro)
    time.sleep(0.5)  # Attente pour éviter d'envoyer des commandes trop rapidement


ser.close()  # Fermer le port série
"""Test de la fonction obtenir_position()"""
import serial
import time

# Configuration du port série
ser = serial.Serial('COM4', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 0.1 # Définir le délai de lecture du port série. Si aucune données n'est détectée passé ce délai, résultat vide ou None

def obtenir_position():
    while True:
        # Lire une ligne de données sérialisées depuis Arduino par le programme gyroscope_calcul_position
        line = ser.readline().decode().strip()
        print("line:", line)

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


print(obtenir_position())

# On dirait que le gyroscope se réinistialise quand on appelle la fonction...
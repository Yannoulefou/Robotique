import serial
import time

# Configuration du port série
ser = serial.Serial('COM4', 115200)  # Remplacez 'COM3' par le port série approprié
ser.timeout = 1  # Définir le délai de lecture du port série

def lecture_gyro():
    # Lire une ligne de données sérialisées depuis Arduino
    values = ser.readline().decode()
    values = values.split(',')
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
            time.sleep(0.1)
            #return (ax, ay, az, gx, gy, gz)
        except ValueError:
            print("Erreur de conversion en float")
    else:
        print("Erreur: la ligne ne contient pas 6 valeurs")
    

while True:
    time.sleep(0.001)
    lecture_gyro()

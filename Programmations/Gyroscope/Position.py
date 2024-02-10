import serial
import telemetrix as tm
import time

# Configuration de la communication série avec Arduino
ser = serial.Serial('COMx', 9600)  # Remplacez 'COMx' par le port série approprié
time.sleep(2)  # Attendez que la connexion série soit établie

# Variables pour la position
pos_x = 0.0
pos_y = 0.0
previous_time = time.time()

# Fonction pour récupérer les données du gyroscope et de l'accéléromètre
def get_sensor_data():
    try:
        # Lire une ligne de données du gyroscope et de l'accéléromètre
        line = ser.readline().decode().strip()
        # Analyser les données à l'aide de Telemetrix
        data = tm.parse(line)
        return data
    except KeyboardInterrupt:
        print("Arrêt de la lecture des données du capteur.")
        ser.close()

# Fonction pour calculer la position
def calculate_position():
    global pos_x, pos_y, previous_time
    while True:
        # Récupérer les données du gyroscope et de l'accéléromètre
        sensor_data = get_sensor_data()
        if sensor_data:
            # Calculer le temps écoulé depuis la dernière mesure
            current_time = time.time()
            delta_time = current_time - previous_time
            previous_time = current_time
            
            # Extraire les accélérations linéaires
            accel_x = sensor_data.get("linear_acceleration_x")
            accel_y = sensor_data.get("linear_acceleration_y")

            # Intégrer les accélérations deux fois pour obtenir la position
            pos_x += accel_x * delta_time**2 / 2
            pos_y += accel_y * delta_time**2 / 2
            
            print("Position (x, y):", pos_x, pos_y)
            
        time.sleep(0.01)  # Attendez 10 ms avant de lire la prochaine donnée

# Appeler la fonction pour calculer la position
calculate_position()

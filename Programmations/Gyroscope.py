import serial
import telemetrix as tm
import time

# Configurer la communication série avec Arduino
ser = serial.Serial('COMx', 9600)  # Remplacez 'COMx' par le port série approprié
time.sleep(2)  # Attendez que la connexion série soit établie

# Fonction pour récupérer les données du gyroscope
def get_gyroscope_data():
    try:
        # Lire une ligne de données du gyroscope
        line = ser.readline().decode().strip()
        # Analyser les données à l'aide de Telemetrix
        data = tm.parse(line)
        return data
    except KeyboardInterrupt:
        print("Arrêt de la lecture des données du gyroscope.")
        ser.close()

# Fonction pour calculer l'angle de rotation
def calculate_rotation_angle():
    previous_angle = 0
    while True:
        # Récupérer les données du gyroscope
        gyro_data = get_gyroscope_data()
        if gyro_data:
            # Extraire la vitesse angulaire du gyroscope
            angular_velocity = gyro_data.get("angular_velocity")
            if angular_velocity is not None:
                # Intégrer la vitesse angulaire pour obtenir l'angle de rotation
                angle = previous_angle + angular_velocity * 0.01  # 0.01 est le pas de temps, ajustez selon votre besoin
                previous_angle = angle
                print("Angle de rotation:", angle)
        time.sleep(0.01)  # Attendez 10 ms avant de lire la prochaine donnée

# Appeler la fonction pour calculer l'angle de rotation
calculate_rotation_angle()

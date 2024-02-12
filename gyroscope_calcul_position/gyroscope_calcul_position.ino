#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

#define DT 0.01  // Temps écoulé depuis la dernière lecture (en secondes)
float x = 0.0;  // Position initiale en x
float y = 0.0;  // Position initiale en y
float angle = PI/2;  // Angle initial

// Initialisation de l'objet MPU6050
Adafruit_MPU6050 mpu;

// Prototypage de la fonction
float* calculer_position(float x_prec, float y_prec, float angle_prec, float ax, float ay, float az, float gx, float gy, float gz);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  Serial.println("Initialisation de l'IMU...");
  if (!mpu.begin()) {
    Serial.println("Échec de l'initialisation de l'IMU");
    while (1);
  }
  Serial.println("IMU initialisée !");
}

void loop() {
  // Lecture des données du gyroscope
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Calcul des valeurs d'accélération (en mm/s²) et de rotation (en radian/s)
  float ax = a.acceleration.x * 1000;
  float ay = a.acceleration.y * 1000;
  float az = a.acceleration.z * 1000;
  float gx = g.gyro.x;
  float gy = g.gyro.y;
  float gz = g.gyro.z;

  // Tableau pour stocker la nouvelle position
  float* nouvelle_position;

  // Calculer la position du robot
  nouvelle_position = calculer_position(x, y, angle, ax, ay, az, gx, gy, gz);
  
  // Mettre à jour les valeurs de position
  x = nouvelle_position[0];
  y = nouvelle_position[1];
  angle = nouvelle_position[2];

  // Libérer la mémoire allouée pour le tableau
  delete[] nouvelle_position;

  // Envoyer les données de position via la liaison série
  Serial.print("Position X: ");
  Serial.print(x);
  Serial.print(" mm, Position Y: ");
  Serial.print(y);
  Serial.print(" mm, Angle: ");
  Serial.print(angle);
  Serial.println(" radians");
  
  // Pause pour permettre à l'IMU de récupérer de nouvelles données
  delay(DT * 1000);
}

float* calculer_position(float x_prec, float y_prec, float angle_prec, float ax, float ay, float az, float gx, float gy, float gz) {
    // Allouer de la mémoire pour le tableau de valeurs de position
    float* nouvelle_position = new float[3];

    // Calcul des valeurs de position
    float x_gyro = ax * (DT * DT);
    float y_gyro = ay * (DT * DT);
    float alpha = 0.49;
    float angle_gyro = alpha * (PI/2 + gx * DT) + alpha * (PI/2 + gy * DT) + (1 - 2 * alpha) * atan2(y_gyro, x_gyro);
    float distance = sqrt(x_gyro * x_gyro + y_gyro * y_gyro);
    float new_angle = angle_prec + angle_gyro - (PI/2);
    float new_x = x_prec + distance * cos(new_angle);
    float new_y = y_prec + distance * sin(new_angle);

    // Stocker les valeurs de position dans le tableau
    nouvelle_position[0] = new_x;
    nouvelle_position[1] = new_y;
    nouvelle_position[2] = new_angle;

    // Retourner le tableau de valeurs de position
    return nouvelle_position;
}

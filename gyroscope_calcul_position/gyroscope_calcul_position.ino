#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

#define DT 0.1  // Temps écoulé depuis la dernière lecture (en secondes)
float x = 0.0;  // Position initiale en x
float y = 0.0;  // Position initiale en y
float angle = PI/2;  // Angle initial
float vx = 0.0;
float vy = 0.0;
float moy_err_ax;
float moy_err_ay;
float moy_err_az;

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

  float somme_err_ax = 0.0;
  float somme_err_ay = 0.0;
  float somme_err_az = 0.0;
  const int nombre_valeurs = 50;

  for (int i = 0; i < nombre_valeurs; i++) {
    // Lecture des données du gyroscope
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Calcul des valeurs d'accélération (en mm/s²)
    float erreur_ax = a.acceleration.x;
    float erreur_ay = a.acceleration.y;
    float erreur_az = a.acceleration.z;

    somme_err_ax += erreur_ax;
    somme_err_ay += erreur_ay;
    somme_err_az += erreur_az;

    delay(50);
  }

  // Calcul de la moyenne
  moy_err_ax = somme_err_ax / nombre_valeurs;
  moy_err_ay = somme_err_ay / nombre_valeurs;
  moy_err_az = somme_err_az / nombre_valeurs;
}

void loop() {
  // Lecture des données du gyroscope
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Calcul des valeurs d'accélération (en mm/s²) et de rotation (en radian/s)
  float ax = (a.acceleration.x-moy_err_ax) * 1000;
  float ay = (a.acceleration.y-moy_err_ay) * 1000;
  float gz = g.gyro.z+0.012;

  // Tableau pour stocker la nouvelle position
  float* nouvelle_position;

  // Calculer la position du robot
  nouvelle_position = calculer_position(x, y, angle, ax, ay, gz, vx, vy);
  
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
  Serial.print(angle*360/(2*PI));
  Serial.println(" degrés");
  
  // Pause pour permettre à l'IMU de récupérer de nouvelles données
  delay(DT * 1000);
}

float* calculer_position(float x_prec, float y_prec, float angle_prec, float ax, float ay, float gz, float vx_prec, float vy_prec) {
    // Allouer de la mémoire pour le tableau de valeurs de position
    float* nouvelle_position = new float[3];

    // Calcul des valeurs de position
    float vx = 0.5*(ax*DT + vx_prec);
    float vy = 0.5*(ay*DT + vy_prec);
    float x_gyro = vx*DT;
    float y_gyro = vy*DT;
    float rotation = gz*DT;
    float new_angle = angle_prec + rotation;
    float new_x = x_prec + (x_gyro*cos(rotation) - y_gyro*sin(rotation));
    float new_y = y_prec + (x_gyro*sin(rotation) + y_gyro*cos(rotation));

    // Stocker les valeurs de position dans le tableau
    nouvelle_position[0] = new_x;
    nouvelle_position[1] = new_y;
    nouvelle_position[2] = new_angle;

    // Retourner le tableau de valeurs de position
    return nouvelle_position;
}

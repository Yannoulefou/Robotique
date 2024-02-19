#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

#define DT 0.1  // Temps écoulé depuis la dernière lecture (en secondes)
float x = 0.0;  // Position initiale en x
float y = 0.0;  // Position initiale en y
float angle = PI/2;  // Angle initial
float vx = 0.0;   // Vitesse initiale en x
float vy = 0.0;   // Vitesse initiale en y

float moy_err_ax = 0.0;   // Erreur moyenne au repos de l'accélération sur l'axe x pour la calibration
float moy_err_ay = 0.0;   // Erreur moyenne au repos de l'accélération sur l'axe y pour la calibration
float moy_err_gz = 0.0;   // Erreur moyenne au repos de la rotation autour de l'axe z pour la calibration

// Initialisation de l'objet MPU6050
Adafruit_MPU6050 mpu;

// Prototypage de la fonction
float* calculer_position(float x_prec, float y_prec, float angle_prec, float ax, float ay, float az, float gx, float gy, float gz);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10); // will pause Zero, Leonardo, etc until serial console opens
  }

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("IMU initialisée !");
  
  float somme_err_ax = 0.0;
  float somme_err_ay = 0.0;
  float somme_err_gz = 0.0;
  const int nombre_valeurs = 100;

  for (int i = 0; i < nombre_valeurs; i++) {
    // Lecture des données du gyroscope
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Calcul des valeurs d'accélération et rotation (en mm/s²)
    float erreur_ax = a.acceleration.x;
    float erreur_ay = a.acceleration.y;
    float erreur_gz = g.gyro.z;

    somme_err_ax += erreur_ax;
    somme_err_ay += erreur_ay;
    somme_err_gz += erreur_gz;

    delay(50);
  }

  // Calcul de la moyenne
  moy_err_ax = somme_err_ax / nombre_valeurs;
  moy_err_ay = somme_err_ay / nombre_valeurs;
  moy_err_gz = somme_err_gz / nombre_valeurs;
}

void loop() {

  // Lecture des données du gyroscope
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Calcul des valeurs d'accélération et rotation (en mm/s² et rad/s)
  float ax = (a.acceleration.x-moy_err_ax)*1000;
  float ay = (a.acceleration.y-moy_err_ay)*1000;
  float gz = g.gyro.z-moy_err_gz;

  // Tableau pour stocker la nouvelle position
  float* nouvelle_position;

  // Calculer la position du robot
  nouvelle_position = calculer_position(x, y, angle, ax, ax, gz, vx, vy);
  
  // Mettre à jour les valeurs de position
  x = nouvelle_position[0];
  y = nouvelle_position[1];
  angle = nouvelle_position[2];
  vx = nouvelle_position[3];
  vy = nouvelle_position[4];

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
  delay(1000*DT);
}


float* calculer_position(float x_prec, float y_prec, float angle_prec, float ax, float ay, float gz, float vx_prec, float vy_prec) {
    // Allouer de la mémoire pour le tableau de valeurs de position
    float* nouvelle_position = new float[5];

    // Calcul des valeurs de position
    float vx = 0.5*(ax*DT + vx_prec + vx_prec);
    float vy = 0.5*(ay*DT + vy_prec + vy_prec);
    float x_gyro = vx*DT;
    float y_gyro = vy*DT;
    float rotation = gz*DT;
    float new_angle = angle_prec + rotation;
    float new_x = x_prec + (x_gyro*cos(new_angle) - y_gyro*sin(new_angle));
    float new_y = y_prec + (x_gyro*sin(new_angle) + y_gyro*cos(new_angle));

    // Stocker les valeurs de position dans le tableau
    nouvelle_position[0] = new_x;
    nouvelle_position[1] = new_y;
    nouvelle_position[2] = new_angle;
    nouvelle_position[3] = vx;
    nouvelle_position[4] = vy;

    // Retourner le tableau de valeurs de position
    return nouvelle_position;
}

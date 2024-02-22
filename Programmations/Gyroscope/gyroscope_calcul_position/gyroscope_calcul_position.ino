#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

#define DT 0.5  // Temps écoulé depuis la dernière lecture (en secondes)
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
Serial.println("Try to initialize !");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("IMU initialisée !");

  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("");
  delay(100);
 
  float somme_err_ax = 0.0;
  float somme_err_ay = 0.0;
  float somme_err_gz = 0.0;
  const int nombre_valeurs = 100;

  for (int i = 0; i < nombre_valeurs; i++) {
    // Lecture des données du gyroscope
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Calcul des valeurs d'accélération et rotation (en m/s²)
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

  const int nb_rep = 50;
  float somme_ax = 0.0;
  float somme_ay = 0.0;
  float somme_gz = 0.0;
  float moy_ax = 0.0;
  float moy_ay = 0.0;
  float moy_gz = 0.0;
  float ax = 0.0;
  float ay = 0.0;
  float gz = 0.0;

  for (int i = 0; i < nb_rep; i++) {
    // Lecture des données du gyroscope
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Calcul des valeurs d'accélération et rotation (en m/s²)
    ax = a.acceleration.x;
    ay = a.acceleration.y;
    gz = g.gyro.z;

    somme_ax += ax;
    somme_ay += ay;
    somme_gz += gz;

    delay(1000*DT/nb_rep);
  }

  moy_ax = somme_ax / nb_rep;
  moy_ay = somme_ay / nb_rep;
  moy_gz = somme_gz / nb_rep;

  // Lecture des données du gyroscope
  // sensors_event_t a, g, temp;
  // mpu.getEvent(&a, &g, &temp);

  // Calcul des valeurs d'accélération et rotation (en mm/s² et rad/s)
  ax = (moy_ax-moy_err_ax)*1000;
  ay = (moy_ay-moy_err_ay)*1000;
  gz = moy_gz-moy_err_gz;

  // Tableau pour stocker la nouvelle position
  float* nouvelle_position;

  // Calculer la position du robot
  nouvelle_position = calculer_position(x, y, angle, ax, ay, gz, vx, vy);
  
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
  // delay(1000*DT);
}


float* calculer_position(float x_prec, float y_prec, float angle_prec, float ax, float ay, float gz, float vx_prec, float vy_prec) {
    // Allouer de la mémoire pour le tableau de valeurs de position
    float* nouvelle_position = new float[5];

    // Calcul des valeurs de position
    float vx = 0.5*ax*DT + vx_prec;
    float vy = 0.5*ay*DT + vy_prec;
    Serial.print("ax :");
    Serial.print(ax);
    Serial.print("   ay :");
    Serial.println(ay);
    Serial.print("vx :");
    Serial.print(vx);
    Serial.print("   vy :");
    Serial.println(vy);
    float x_gyro = vx*DT;
    float y_gyro = vy*DT;
    Serial.print("x_gyro :");
    Serial.print(x_gyro);
    Serial.print("   y_gyro :");
    Serial.println(y_gyro); 
    float rotation = gz*DT;
    float new_angle = angle_prec + rotation;
    float new_x = x_prec + (x_gyro*cos(new_angle - PI/2) - y_gyro*sin(new_angle - PI/2));
    float new_y = y_prec + (x_gyro*sin(new_angle - PI/2) + y_gyro*cos(new_angle - PI/2));

    // Stocker les valeurs de position dans le tableau
    nouvelle_position[0] = new_x;
    nouvelle_position[1] = new_y;
    nouvelle_position[2] = new_angle;
    nouvelle_position[3] = vx;
    nouvelle_position[4] = vy;

    // Retourner le tableau de valeurs de position
    return nouvelle_position;
}

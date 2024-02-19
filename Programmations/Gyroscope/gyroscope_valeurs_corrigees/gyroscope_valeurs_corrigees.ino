#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

float moy_err_ax = 0.0;
float moy_err_ay = 0.0;
float moy_err_az = 0.0;
float moy_err_gx = 0.0;
float moy_err_gy = 0.0;
float moy_err_gz = 0.0;

// Initialisation de l'objet MPU6050
Adafruit_MPU6050 mpu;

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
  float somme_err_ax = 0.0;
  float somme_err_ay = 0.0;
  float somme_err_az = 0.0;
  float somme_err_gx = 0.0;
  float somme_err_gy = 0.0;
  float somme_err_gz = 0.0;
  const int nombre_valeurs = 100;

  for (int i = 0; i < nombre_valeurs; i++) {
    // Lecture des données du gyroscope
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Calcul des valeurs d'accélération et rotation (en mm/s²)
    float erreur_ax = a.acceleration.x;
    float erreur_ay = a.acceleration.y;
    float erreur_az = a.acceleration.z;
    float erreur_gx = g.gyro.x;
    float erreur_gy = g.gyro.y;
    float erreur_gz = g.gyro.z;

    somme_err_ax += erreur_ax;
    somme_err_ay += erreur_ay;
    somme_err_az += erreur_az;
    somme_err_gx += erreur_gx;
    somme_err_gy += erreur_gy;
    somme_err_gz += erreur_gz;

    delay(50);
  }

  // Calcul de la moyenne
  moy_err_ax = somme_err_ax / nombre_valeurs;
  moy_err_ay = somme_err_ay / nombre_valeurs;
  moy_err_az = somme_err_az / nombre_valeurs;
  moy_err_gx = somme_err_gx / nombre_valeurs;
  moy_err_gy = somme_err_gy / nombre_valeurs;
  moy_err_gz = somme_err_gz / nombre_valeurs;
}



void loop() {
  
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  Serial.print(a.acceleration.x-moy_err_ax);
  Serial.print(",");
  Serial.print(a.acceleration.y-moy_err_ay);
  Serial.print(",");
  Serial.print(a.acceleration.z-moy_err_az);
  Serial.print(",");
  Serial.print(g.gyro.x-moy_err_gx);
  Serial.print(",");
  Serial.print(g.gyro.y-moy_err_gy);
  Serial.print(",");
  Serial.print(g.gyro.z-moy_err_gz);
  Serial.println("");

  delay(1000);
}

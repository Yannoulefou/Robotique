#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h> // pour utiliser PI
#include <Arduino.h>
#include <HC_SR04.h>
// AccelStepper https://www.youtube.com/watch?v=QRCvC5xhJCw
// Pour éviter la surchauffe des moteurs Vref https://www.youtube.com/watch?v=BV-ouxhZamI
// Taille de roue 76mm https://www.decathlonpro.fr/paire-roues-oxeloboard-roulements-id-8127600.html

// Mesures
const int roue = 76; // diamètre de la roue en mm
const int essieu = 203; // distance entre les deux roues en mm (vraie distance : 200, mais ajustée pour que le robot tourne du bon angle)
const int xmax = 3000;
const int ymax = 2000;
const int pas_par_tour = 200; // nombre de pas à effectuer pour réaliser un tour

/*
STEP, DIR
X : 2, 5 (Left)
Y: 3, 6 (Right)
Z: 4, 7
*/

const int enPin = 8; // enable Pin pour allumer le shield
AccelStepper stepper_L(1, 4, 7);  // 1=using_controller, pull, dir
AccelStepper stepper_R(1, 3, 6);


// Pour les étapes
int etape = 0;
unsigned long startTime = 0;

// Define Ultrason
#define TRIG_PIN 5
#define ECHO_PIN 2
HC_SR04<ECHO_PIN> sensor(TRIG_PIN);   // sensor with echo and trigger pin
signed long distance;
// unsigned long interval_ultrason;



void setup() {
 	Serial.begin(9600);
  // Allumer le shield
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  // setup Left
  stepper_L.setMaxSpeed(200.0);
  stepper_L.setAcceleration(200.0);
  // setup Right
  stepper_R.setMaxSpeed(200.0);
  stepper_R.setAcceleration(200.0);

  // Initalize Ultrason
  sensor.beginAsync();  
  sensor.startAsync(100000);        // start first measurement
  // pinMode(TRIG_PIN, OUTPUT);
  // pinMode(ECHO_PIN, INPUT);
  // interval_ultrason = micros();
  distance = -1;
  Serial.println(distance);
  Serial.println("Setup");
  
}

void loop() {
  ultrason_nonbloquant();
  // Pause execution for 1 second (1000 milliseconds)  
  if (stepper_L.distanceToGo() == 0 && stepper_R.distanceToGo() == 0 ) {
    Serial.println();
    Serial.print("Etape : ");
    Serial.println(etape);
    if (etape==0) {
      // Cache Ultrason
      if (distance != -1 && distance >10) {
        etape = 1;
        startTime=micros();
      }
    } else if (etape == 1) {
      // Avancer 1.7m soit 1700 mm
      avance(2000);
      etape = 4;
    } else if (etape == 2) {
      // Tourner de 45°
      turn(PI/4);
      etape = 3;
    } else if (etape == 3) {
      // Avancer de 1m
      avance(1200);
      etape = 4;
    } else if (etape == 4) {
      // Desactivation des moteurs
      digitalWrite(enPin, HIGH);
    }
  }
  
  bool run = true;
  if (distance != -1 && distance < 20) {
    Serial.println("Obstacle detecté");
    run = false;
  }
  if (micros()-startTime > 95000000) {// 95secondes
    run = false;
    etape = 4;
  }
  // Run motor
  if (run) {
  stepper_L.run();
  stepper_R.run();
  }
}



void turn(float angle) { 
  // left = +-1, si = +1, alors le moteur gauche recule et le droit avance pour tourner à gauche

  // Calcul du nombre de pas à effectuer
  long steps = (pas_par_tour * angle*essieu) / (2*PI*roue);
  Serial.println("New turn");
  // Move both stepper motors simultaneously
    stepper_L.moveTo(stepper_L.currentPosition() + steps);
    stepper_R.moveTo(stepper_R.currentPosition() - steps);
}

void avance(float distance) {
  long steps = (pas_par_tour * distance) / (PI*roue);
  Serial.println("New line");
  stepper_L.moveTo(stepper_L.currentPosition() + steps);
  stepper_R.moveTo(stepper_R.currentPosition() + steps);
}

void ultrason() {
  
  long duration;
  // Envoie une impulsion ultrasonique
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // Mesure la durée de l'impulsion ultrasonique
  duration = pulseIn(ECHO_PIN, HIGH);
  
  // Convertit la durée en distance (en cm)
  distance = duration * 0.034 / 2;
  if (distance < 2 || distance > 400) {
    distance = -1;
  } 
  
  // Affiche la distance mesurée sur le moniteur série
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
}

void ultrason_nonbloquant() {
  if (sensor.isFinished()) {
    distance = sensor.getDist_cm();
    if (distance < 2 || distance > 400) {
      distance = -1;
    } 
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  sensor.startAsync(100000);
  }
}


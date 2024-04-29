#include <AccelStepper.h>
#include <math.h> // pour utiliser PI
// AccelStepper https://www.youtube.com/watch?v=QRCvC5xhJCw
// Pour éviter la surchauffe des moteurs Vref https://www.youtube.com/watch?v=BV-ouxhZamI
// Taille de roue 76mm https://www.decathlonpro.fr/paire-roues-oxeloboard-roulements-id-8127600.html

// Mesures
const int roue = 76; // diamètre de la roue en mm
const int essieu = 450; // distance entre les deux roues en mm
const int xmax = 3000;
const int ymax = 2000;
const int pas_par_tour = 200; // nombre de pas à effectuer pour réaliser un tour

bool line = true;

/*
STEP, DIR
X : 2, 5 (Left)
Y: 3, 6 (Right)
Z: 4, 7
*/

const int enPin = 8; // enable Pin pour allumer le shield
AccelStepper stepper_L(1, 2, 5);  // 1=using_controller, pull, dir
AccelStepper stepper_R(1, 3, 6);

void setup() {
 	Serial.begin(9600);
  // Allumer le shield
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  // setup Left
  stepper_L.setMaxSpeed(100.0);
  stepper_L.setAcceleration(50.0);
  // setup Right
  stepper_R.setMaxSpeed(100.0);
  stepper_R.setAcceleration(50.0);
}

void loop() {
  // Pause execution for 1 second (1000 milliseconds)  
  if (stepper_L.distanceToGo() == 0 && stepper_R.distanceToGo() == 0 ) {
    delay(1000);
    if (line) {
    stepper_L.moveTo(stepper_L.currentPosition() - 400);
    stepper_R.moveTo(stepper_R.currentPosition() - 400);
    line = false;

    } else {
    turn(PI/2);
    line = true;

    }

  }
  
  // Run motor
  stepper_L.run();
  stepper_R.run();

}



void turn(float angle) { 
  // left = +-1, si = +1, alors le moteur gauche recule et le droit avance pour tourner à gauche

  // Calcul du nombre de pas à effectuer
  long steps = pas_par_tour * (angle / (2*PI)) * (essieu / roue);
  Serial.println("New turn");
  Serial.println(stepper_L.currentPosition());
  Serial.println(stepper_R.currentPosition());
  // Move both stepper motors simultaneously
    stepper_L.moveTo(stepper_L.currentPosition() + steps);
    stepper_R.moveTo(stepper_R.currentPosition() - steps);
}





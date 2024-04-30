#include <AccelStepper.h>
// https://www.youtube.com/watch?v=QRCvC5xhJCw
// Pour éviter la surchauffe des moteurs Vref https://www.youtube.com/watch?v=BV-ouxhZamI

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
  // Allumer le shield
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  // setup Left
  stepper_L.setMaxSpeed(400.0);
  stepper_L.setAcceleration(100.0);
  stepper_L.moveTo(300);
  // setup Right
  stepper_R.setMaxSpeed(400.0);
  stepper_R.setAcceleration(100.0);
  stepper_R.moveTo(300);
}

void loop() {

  // Change direction at the limits
  if (stepper_L.distanceToGo() == 0 && stepper_R.distanceToGo() == 0 ) {
    stepper_L.moveTo(-stepper_L.currentPosition());
    stepper_R.moveTo(-stepper_R.currentPosition());

  }
  stepper_L.run();
  stepper_R.run();
}
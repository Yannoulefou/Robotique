#include <AccelStepper.h>
// https://www.youtube.com/watch?v=QRCvC5xhJCw

/*
STEP, DIR
X : 2, 5
Y: 3, 6
Z: 4, 7
*/

#define pul1 2
#define dir1 5
const int enPin=8;
AccelStepper stepper1(1, 2, 5); // 1=using_controller, pull, dir
AccelStepper stepper2(1, 3, 6);
 
void setup()
{  
 	pinMode(enPin, OUTPUT);
 	digitalWrite(enPin, LOW);
    stepper1.setMaxSpeed(200.0);
    stepper1.setAcceleration(100.0);
    stepper1.moveTo(24);
    
    stepper2.setMaxSpeed(300.0);
    stepper2.setAcceleration(100.0);
    stepper2.moveTo(1000000);


}
 
void loop()
{
    // Change direction at the limits
    if (stepper1.distanceToGo() == 0)
        stepper1.moveTo(-stepper1.currentPosition());
    stepper1.run();
    stepper2.run();
}
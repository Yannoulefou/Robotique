#include <Stepper.h>

// Définir le nombre de pas par tour
int NbrPas = 200; 


Stepper MonMoteur(NbrPas, 8, 9, 10, 11);

void setup() {
  // Vitesse à 60 tours/min
  MonMoteur.setSpeed(60);
 
  Serial.begin(9600);
}

void loop() {
  // Faire un tour dans un sens
  Serial.println("Sens 1");
  MonMoteur.step(NbrPas);
  delay(500);

  // Faire un tour dans l'autre sens
  Serial.println("Sens 2");
  MonMoteur.step(-NbrPas);
  delay(500);
}
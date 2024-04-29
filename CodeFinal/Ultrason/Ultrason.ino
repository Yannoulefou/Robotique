#define TRIG_PIN 11
#define ECHO_PIN 13

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);+
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  long duration, distance;
  
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
  
  // Affiche la distance mesurée sur le moniteur série
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  delay(1000); // Attendre 1 seconde avant la prochaine mesure
}

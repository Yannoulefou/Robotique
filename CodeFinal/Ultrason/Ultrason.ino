#define TRIG_PIN 13
#define ECHO_PIN 11

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  long duration, distance, startTime;
  startTime = micros();
  // Envoie une impulsion ultrasonique
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  Serial.print("Impulsion : ");
  Serial.println(micros()-startTime);
  
  startTime = micros();
  // Mesure la durée de l'impulsion ultrasonique
  duration = pulseIn(ECHO_PIN, HIGH);
  Serial.print("pulseIn : ");
  Serial.println(micros()-startTime);
  
  // Convertit la durée en distance (en cm)
  distance = duration * 0.034 / 2;
  
  // Affiche la distance mesurée sur le moniteur série
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  delay(1000); // Attendre 1 seconde avant la prochaine mesure
}

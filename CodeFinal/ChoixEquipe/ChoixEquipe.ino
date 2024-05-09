
const int positif = 10; // Y-limit switch
const int readPin = 11; // Z-limit switch




void setup() {
  // put your setup code here, to run once:
  pinMode(positif, OUTPUT);
  digitalWrite(positif, HIGH);
  
  pinMode(readPin, INPUT_PULLUP);

  
 	Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int team_value = digitalRead(readPin);
  Serial.println(team_value);

  delay(1000);
}

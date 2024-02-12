#define STEP_PIN 2
#define DIR_PIN 3
#define ENABLE_PIN 4

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  digitalWrite(ENABLE_PIN, LOW); // Enable the driver
}

void loop() {
  // Set direction (HIGH for clockwise, LOW for counterclockwise)
  digitalWrite(DIR_PIN, HIGH);

  // Step the motor (adjust delay for desired speed)
  for (int i = 0; i < 1000; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(750); // Adjust delay based on motor speed
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(750); // Adjust delay based on motor speed
  }

  // Pause between movements
  delay(1000);

  // Reverse direction
  digitalWrite(DIR_PIN, LOW);

  // Step the motor in the opposite direction
  for (int i = 0; i < 1000; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000); // Adjust delay based on motor speed
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000); // Adjust delay based on motor speed
  }

  // Pause between movements
  delay(1000);
}

#define DIR_G_PIN 2
#define STEP_G_PIN 3
#define ENABLE_G_PIN 4

#define DIR_D_PIN 5
#define STEP_D_PIN 6
#define ENABLE_D_PIN 7

void setup() {
  pinMode(DIR_G_PIN, OUTPUT);
  pinMode(STEP_G_PIN, OUTPUT);
  pinMode(ENABLE_G_PIN, OUTPUT);
  
  pinMode(DIR_D_PIN, OUTPUT);
  pinMode(STEP_D_PIN, OUTPUT);
  pinMode(ENABLE_D_PIN, OUTPUT);

  digitalWrite(ENABLE_G_PIN, LOW); // Enable the driver
  digitalWrite(ENABLE_D_PIN, LOW); // Enable the driver
}

void loop() {
  // Set direction (HIGH for clockwise, LOW for counterclockwise)
  digitalWrite(DIR_G_PIN, HIGH);

  // Step the motor (adjust delay for desired speed)
  for (int i = 0; i < 1000; i++) {
    digitalWrite(STEP_G_PIN, HIGH);
    delayMicroseconds(750); // Adjust delay based on motor speed
    digitalWrite(STEP_G_PIN, LOW);
    delayMicroseconds(750); // Adjust delay based on motor speed
  }

  // Pause between movements
  delay(1000);

  // Reverse direction
  digitalWrite(DIR_G_PIN, LOW);

  // Step the motor in the opposite direction
  for (int i = 0; i < 1000; i++) {
    digitalWrite(STEP_G_PIN, HIGH);
    delayMicroseconds(1000); // Adjust delay based on motor speed
    digitalWrite(STEP_G_PIN, LOW);
    delayMicroseconds(1000); // Adjust delay based on motor speed
  }

  // Pause between movements
  delay(1000);
}

// Pins
const int TRIG = 4;      // Trigger pin
const int ECHO = 3;      // Echo pin
const int LED = 5;      // Onboard LED (D13)

long duration;
float distance;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600); // Serial monitor
}

float getDistance() {
  // Clear the trigger
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  // Send a 10us pulse
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  // Read echo pulse duration
  duration = pulseIn(ECHO, HIGH, 30000); // timeout 30ms

  // Calculate distance in cm
  distance = (duration * 0.0343) / 2;
  return distance;
}

void loop() {
  float dist = getDistance();
  Serial.print("Distance: ");
  Serial.print(dist);
  Serial.println(" cm");

  if (dist > 10 && dist < 70) {
    // Blink LED quickly twice
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    digitalWrite(LED, HIGH);
    delay(40);
    digitalWrite(LED, LOW);
    delay(5);
  }
  else if (dist > 10 && dist < 100) {
    // Blink LED quickly twice
    digitalWrite(LED, HIGH);
    delay(50);
    digitalWrite(LED, LOW);
    delay(20);
  } else {
    digitalWrite(LED, LOW); // LED off
    delay(5);
  }
}

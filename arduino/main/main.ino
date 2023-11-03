#include <SoftwareSerial.h>
SoftwareSerial bluetoothSerial(9, 10); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11

// Motor A
const int motor1Pin1 = 2; // IN1 on the L293D
const int motor1Pin2 = 4; // IN2 on the L293D
const int enableMotor1 = 3; // EN1 on the L293D

// Motor B
const int motor2Pin1 = 7; // IN3 on the L293D
const int motor2Pin2 = 8; // IN4 on the L293D
const int enableMotor2 = 5; // EN2 on the L293D

int throttle = 0, turn = 0;
unsigned long lastInputTimestamp;

void setup() {
  bluetoothSerial.begin(57600); //Baudrate 57600 , Choose your own baudrate 
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
}

void parseSerialInput() {
  String str = String((char) bluetoothSerial.read());
  while (str.charAt(str.length() - 1) != '\n' && bluetoothSerial.available() > 0) {
    str += (char) bluetoothSerial.read();
  }
  sscanf(str.c_str(), "%d,%d\n", &throttle, &turn);
  lastInputTimestamp = millis();
}

void driveMotors(int throttle, int turn) {
  // Calculate the speed for each motor
  int speedMotor1 = throttle + turn;
  int speedMotor2 = throttle - turn;

  // Constrain speeds to -255 to 255
  speedMotor1 = constrain(speedMotor1, -255, 255);
  speedMotor2 = constrain(speedMotor2, -255, 255);

  // Adjust for the motor direction
  if (speedMotor1 > 0) {
    analogWrite(enableMotor1, speedMotor1);
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
  } else {
    analogWrite(enableMotor1, -speedMotor1); // speedMotor1 is negative
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
  }

  // Adjust for the motor direction
  if (speedMotor2 > 0) {
    analogWrite(enableMotor2, speedMotor2);
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
  } else {
    analogWrite(enableMotor2, -speedMotor2); // speedMotor2 is negative
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
  }
}

void loop() {
  bool btAvailable = bluetoothSerial.available() > 0;
  if(btAvailable) {
    parseSerialInput();
  }

  // Print out values
  Serial.print(throttle);
  Serial.print(" ");
  Serial.println(turn);

  // Adjust motor output
  driveMotors(throttle, turn);
  
  if (!btAvailable) {
    // Reset drive values if no inputs after 500ms
    if (millis() - lastInputTimestamp > 500) {
      Serial.println("reset!");
      throttle = 0;
      turn = 0;

      lastInputTimestamp = millis();
    }

    // We run this delay statement after everything so we always act on newest data on loop iter
    // Serial.println("waiting for input...");
    delay(25);
  }
}
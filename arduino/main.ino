#include <SoftwareSerial.h>
SoftwareSerial bluetoothSerial(9, 10); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11

int LED = 13; //Use whatever pins you want 
int throttle = 0, turn = 0;

int lastInputTimestamp;

void setup() {
  bluetoothSerial.begin(57600); //Baudrate 9600 , Choose your own baudrate 
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

void loop() {
  bool btAvailable = bluetoothSerial.available() > 0;
  if(btAvailable) {
    parseSerialInput();
  }

  // Print out values
  Serial.print(throttle);
  Serial.print(" ");
  Serial.println(turn);

  // TODO: Adjust PWM output on motors
  
  if (!btAvailable) {
    // Reset drive values if no inputs after 100ms
    if (millis() - lastInputTimestamp > 100) {
      throttle = 0;
      turn = 0;
    }

    // We run this delay statement after everything so we always act on newest data on loop iter
    Serial.println("waiting for input...");
    delay(25);
  }
}
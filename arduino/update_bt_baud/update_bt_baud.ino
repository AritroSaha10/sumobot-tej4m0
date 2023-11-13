#include <SoftwareSerial.h>
SoftwareSerial BT(9, 10); // TX to pin_10. RX to pin_11 of Arduino.
    
void setup() {
    Serial.begin(9600);
    BT.begin(9600);
    delay(1000);
    BT.write("AT+BAUD7"); // 57600
}

void loop() {

}
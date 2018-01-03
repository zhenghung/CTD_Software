int led = 13;
int incomingByte = 0;

void setup() {
    pinMode(led, OUTPUT);
    
    //Setup Serial Port with baud rate of 9600
    Serial.begin(9600);
    Serial.println("Press H to turn LED ON");
    Serial.println("Press L to turn LED OFF");
}

void loop() {
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
    
        if(incomingByte == 'H'){
            digitalWrite(led, HIGH);
            Serial.println("LED ON");
        }else if(incomingByte == 'L'){
            digitalWrite(led, LOW);
            Serial.println("LED OFF");
        }else{
            Serial.println("invalid!");
        }
      
    }
}

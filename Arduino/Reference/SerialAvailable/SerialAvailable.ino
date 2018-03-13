
unsigned long a = 0;
bool b = true;

void setup() {
  Serial.begin(9600);
}

void loop() {
  while(b){
    int num = Serial.available();
    if(num>0){
      char c = Serial.read();

      Serial.print("num: ");
      Serial.println(c);
      b = false;
      break;
    }
    Serial.println(a);
    a = millis();
    delay(100);
  }
}

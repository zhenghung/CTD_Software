int led = 13;
int incomingByte = 0;
int count = 0;
int state = 0;

void setup() {
    pinMode(led, OUTPUT);
    //Setup Serial Port with baud rate of 9600
    Serial.begin(9600);
}

void loop() {
  if(state==0){
    for(int i=0; i<=20; i++){
      Serial.print("Number: ");
      Serial.println(i);
      delay(300);
    }
    state=1;
  }else{
    while(Serial.available()){
      Serial.println("Number: 55");
      if(Serial.read()=='A'){
        state=0;
      }
    }

      
  }
    
    
}

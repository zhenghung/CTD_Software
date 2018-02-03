int led = 13;
int incomingByte = 0;
int measure = 0;
int tally =0;
int repeat;

void setup() {
    pinMode(led, OUTPUT);
    pinMode(A0, INPUT);
    //Setup Serial Port with baud rate of 9600
    Serial.begin(9600);
    repeat=0;
}

void loop() {
      
    measure = analogRead(A0);
    if(measure>800){
//      Serial.println("HIT");
      if(repeat == 0){
        repeat =  1;
        tally++;
      }
      
    }else{
//      Serial.println("MISS");
      if(repeat == 1){
        repeat =  0;
        tally++;
      }
    }
    Serial.println(measure);
}

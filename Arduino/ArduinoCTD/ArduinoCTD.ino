enum state_enum {COM_STANDBY, COM_M1, COM_M2, MOI_STANDBY, MOI_M1, MOI_M2, MOI_M3};
enum action_enum {CHGMOI, CHGCOM, BEGIN_COM1, BEGIN_COM2, COM_DONE, BEGIN_MOI1, BEGIN_MOI2, BEGIN_MOI3, MOI_DONE, RESET};

int serialInput;
state_enum state = COM_STANDBY;
action_enum action;

#define loadcellA A0
#define loadcellB A1
#define loadcellC A2
#define tachometer A3
#define led 10

void setup() {
  pinMode(loadcellA, INPUT);
  pinMode(loadcellB, INPUT);
  pinMode(loadcellC, INPUT);
  pinMode(tachometer, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  state_machine(listeningLoop());
  delay(10);
}

void state_machine(uint8_t action){
  switch(state){
    case COM_STANDBY:
      if(action == CHGMOI){
        state = MOI_STANDBY;
        Serial.println("moichged");
      }
      else if(action == BEGIN_COM1){
        state = COM_M1;
        com_measure(0);
      }
  }
}

uint8_t listeningLoop(){
  while(Serial.available()>0){
    serialInput = Serial.read();
    switch(serialInput){
      case 'M0':
        return CHGMOI;
        break;
      case 'C0':
        return CHGCOM;
        break;
      case 'C1':
        return BEGIN_COM1;
        break;
      case 'C2':
        return BEGIN_COM2;
        break;  
      case 'C9':
        return COM_DONE;
        break;  
      case 'M1':
        return BEGIN_MOI1;
        break;
      case 'M2':
        return BEGIN_MOI2;
        break;
      case 'M3':
        return BEGIN_MOI3;
        break;
      case 'M9':
        return MOI_DONE;
        break;  
      case 'RS':
        return RESET;
        break;
    }
  }
}

void com_measure(int orientation){
  /* READ PIN VALUES AND CONVERT TO newtons? */
  /* Serial print 3 values for each load cell*/
}
void moi_measure(int orientation){
  /* START TIMER AS SOON AS PIN VALUE CHANGES - BEGIN OSCILLATION*/
  /* TALLY NUMBER OF OSCILLATIONS */
  /* AFTER A CERTAIN OSCILLATION, STOP TIMING */
  /* SERIAL PRINT TOTAL TIME AND AVERAGE PERIOD */
}

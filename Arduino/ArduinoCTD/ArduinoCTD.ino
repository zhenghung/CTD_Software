enum state_enum {STARTUP, COM_STANDBY, COM_M1, COM_M2, MOI_STANDBY, MOI_M1, MOI_M2, MOI_M3};
enum action_enum {CHGCOM, BEGIN_COM1, BEGIN_COM2, COM_DONE, CHGMOI, BEGIN_MOI1, BEGIN_MOI2, BEGIN_MOI3, MOI_DONE, RESET};

int serialInput;
int firstLaunch = true;
state_enum state = STARTUP;
action_enum action;

#define LOADCELLA A0
#define LOADCELLB A1
#define LOADCELLC A2
#define tachometer A3
#define led 10

int loadCellA;
int loadCellB;
int loadCellC;
int oscillations;

void setup() {
  pinMode(LOADCELLA, INPUT);
  pinMode(LOADCELLB, INPUT);
  pinMode(LOADCELLC, INPUT);
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
    case STARTUP:
      if(firstLaunch){
        Serial.println("STARTUP");
        firstLaunch = false;
      }
      if(action == CHGCOM){
        state = COM_STANDBY;
        Serial.println("CHGCOM");
      }
      if(action == CHGMOI){
        state = MOI_STANDBY;
        Serial.println("CHGMOI");
      }
      break;
    case COM_STANDBY:
      if(action == CHGMOI){
        state = MOI_STANDBY;
        Serial.println("CHGMOI");
      }
      else if(action == BEGIN_COM1){
        state = COM_M1;
        Serial.println("BEGIN_COM1");
        com_measure(0);
      }
      else if(action == RESET){
        state = COM_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;
    case COM_M1:
      if(action == BEGIN_COM2){
        state = COM_M2;
        Serial.println("BEGIN_COM2");
        com_measure(1);        
      }
      else if(action == RESET){
        state = COM_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;
    case COM_M2:
      if(action == COM_DONE){
        state = COM_STANDBY;
        Serial.println("COM_DONE");       
      }
      else if(action == RESET){
        state = COM_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;
    case MOI_STANDBY:
      if(action == CHGCOM){
        state = COM_STANDBY;
        Serial.println("CHGCOM");
      }
      else if(action == BEGIN_MOI1){
        state = MOI_M1;
        Serial.println("BEGIN_MOI1");
        moi_measure(0);
      }
      else if(action == RESET){
        state = MOI_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;
    case MOI_M1:
      if(action == BEGIN_MOI2){
        state = MOI_M2;
        Serial.println("BEGIN_MOI2");
        moi_measure(1);        
      }
      else if(action == RESET){
        state = MOI_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;
    case MOI_M2:
      if(action == BEGIN_MOI3){
        state = MOI_M3;
        Serial.println("BEGIN_MOI3");
        moi_measure(2);        
      }
      else if(action == RESET){
        state = MOI_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;
    case MOI_M3:
      if(action == MOI_DONE){
        state = MOI_STANDBY;
        Serial.println("MOI_DONE");        
      }
      else if(action == RESET){
        state = MOI_STANDBY;
        Serial.println("RESET");
      }
      else{
        
      }
      break;      
  }
}

/*
 * Action Function
 * listens to serial and apply action respectively
 * [  'Q' ,    'W'   ,    'E'   ,   'R'  ]
 * [CHGCOM,BEGIN_COM1,BEGIN_COM2,COM_DONE] 
 *
 * [  'A' ,    'S'   ,    'D'   ,    'F'   ,  'G'   ]
 * [CHGMOI,BEGIN_MOI1,BEGIN_MOI2,BEGIN_MOI3,MOI_DONE] 
 */
uint8_t listeningLoop(){
  while(Serial.available()>0){
    serialInput = Serial.read();
    switch(serialInput){
      case 'Q':
        return CHGCOM;
      case 'W':
        return BEGIN_COM1;
      case 'E':
        return BEGIN_COM2;
      case 'R':
        return COM_DONE;
      case 'A':
        return CHGMOI;
      case 'S':
        return BEGIN_MOI1;
      case 'D':
        return BEGIN_MOI2;
      case 'F':
        return BEGIN_MOI3;
      case 'G':
        return MOI_DONE;
      case '0':
        return RESET;
      default:
        Serial.println("WRONG_INPUT");
        break;
    }
  }
}

void com_measure(int orientation){
  /* READ PIN VALUES AND CONVERT TO newtons? */
  /* SERIAL print 3 values for each load cell*/
  loadCellA = 100;
  loadCellB = 100;
  loadCellC = 100;
  Serial.print("A: ");
  Serial.println(loadCellA);
  Serial.print("B: ");
  Serial.println(loadCellB);
  Serial.print("C: ");
  Serial.println(loadCellC);
}
void moi_measure(int orientation){
  /* START TIMER AS SOON AS PIN VALUE CHANGES - BEGIN OSCILLATION*/
  /* TALLY NUMBER OF OSCILLATIONS */
  /* AFTER A CERTAIN OSCILLATION, STOP TIMING */
  /* SERIAL PRINT TOTAL TIME AND AVERAGE PERIOD */
  delay(3000);
  oscillations = 10;
  Serial.print("OSC: ");
  Serial.println(oscillations);
}

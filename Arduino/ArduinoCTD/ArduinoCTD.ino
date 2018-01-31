#include "HX711.h"

HX711 cellA;
HX711 cellB;
HX711 cellC;

enum state_enum {STARTUP, COM_STANDBY, COM_M1, COM_M2, MOI_STANDBY, MOI_M1, MOI_M2, MOI_M3};
enum action_enum {CHGCOM, BEGIN_COM1, BEGIN_COM2, COM_DONE, CHGMOI, BEGIN_MOI1, BEGIN_MOI2, BEGIN_MOI3, MOI_DONE, RESET, TARE, INVALID};

int serialInput;
int firstLaunch = true;
state_enum state = STARTUP;
action_enum action;
action_enum prevAction;

#define LOADCELLA A0
#define LOADCELLB A1
#define LOADCELLC A2
#define tachometer A3
#define led 10

float loadCellA;
float loadCellB;
float loadCellC;
float oscillations;


void setup() {
  cellA.begin(7,6); // PIN7 is DT, PIN6 is SCK
  cellA.set_scale(477.f);
  cellA.tare();
  cellB.begin(5,4); // PIN5 is DT, PIN4 is SCK
  cellB.set_scale(450.f);
  cellB.tare();
  cellC.begin(3,2); // PIN3 is DT, PIN2 is SCK
  cellC.set_scale(440.f);
  cellC.tare();
  // pinMode(LOADCELLB, INPUT);
  // pinMode(LOADCELLC, INPUT);
  // pinMode(tachometer, INPUT);
  // pinMode(led, OUTPUT);
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
        tareCells();
      }
      if(action == CHGCOM){
        state = COM_STANDBY;
        Serial.println("CHGCOM");
        tareCells();
        prevAction = CHGCOM;
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
        prevAction = CHGMOI;
      }
      else if(action == BEGIN_COM1){
        state = COM_M1;
        Serial.println("BEGIN_COM1");
        com_measure(0);
        prevAction = BEGIN_COM1;
      }
      else if(action == RESET){
        state = COM_STANDBY;
        Serial.println("RESET");
        prevAction = RESET;
      }
      else if(action == TARE){
        if(prevAction != TARE){
          tareCells();
          // Serial.println("TAREDONE");
          action = INVALID; 
          prevAction = TARE; 
        }   
      }
      else{
        
      }
      break;
    case COM_M1:
      if(action == BEGIN_COM2){
        state = COM_M2;
        Serial.println("BEGIN_COM2");
        com_measure(1);      
        prevAction = BEGIN_COM2;
      }
      else if(action == RESET){
        state = COM_STANDBY;
        Serial.println("RESET");
        tareCells();
        prevAction = RESET;
      }
      else if(action == TARE){
        if(prevAction != TARE){
          tareCells();
          // Serial.println("TAREDONE");
          action = INVALID; 
          prevAction = TARE; 
        }
      }
      else{
        
      }
      break;
    case COM_M2:
      if(action == COM_DONE){
        state = COM_STANDBY;
        Serial.println("COM_DONE"); 
        prevAction = COM_DONE;    
      }
      else if(action == RESET){
        state = COM_STANDBY;
        Serial.println("RESET");
        tareCells();
        prevAction = RESET;
      }
      else if(action == TARE){
        if(prevAction != TARE){
          tareCells();
          // Serial.println("TAREDONE");
          action = INVALID; 
          prevAction = TARE; 
        }
      }
      else{
        
      }
      break;
    case MOI_STANDBY:
      if(action == CHGCOM){
        state = COM_STANDBY;
        Serial.println("CHGCOM");
        tareCells();
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
 * [  'Q' ,    'W'   ,    'E'   ,   'R'  , 'T']
 * [CHGCOM,BEGIN_COM1,BEGIN_COM2,COM_DONE,TARE] 
 *
 * [  'A' ,    'S'   ,    'D'   ,    'F'   ,  'G'   ]
 * [CHGMOI,BEGIN_MOI1,BEGIN_MOI2,BEGIN_MOI3,MOI_DONE] 
 */
uint8_t listeningLoop(){
  if(Serial.available()>0){
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
      case 'T':
        return TARE;
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
  loadCellA = cellA.get_units(20);
  loadCellB = cellB.get_units(20);
  loadCellC = cellC.get_units(20);
  Serial.print("A: ");
  Serial.println(loadCellA, 2);
  Serial.print("B: ");
  Serial.println(loadCellB, 2);
  Serial.print("C: ");
  Serial.println(loadCellC, 2);
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

void tareCells(){
  cellA.tare();
  cellB.tare();
  cellC.tare();
  Serial.println("TAREDONE");
}
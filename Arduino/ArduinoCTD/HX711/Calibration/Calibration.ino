#include "HX711.h"

HX711 cellA;
HX711 cellB;
HX711 cellC;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 Demo");
  Serial.println("Initializing the scale");

  // cell#.begin( DT , SCK)
  cellA.begin(7, 6);
  cellB.begin(5, 4);
  cellC.begin(3, 2);

  // Change these till measured weight is accurate
  cellA.set_scale(452.f);
  cellB.set_scale(442.f);
  cellC.set_scale(453.5f);

  delay(2000);  // Delay 2 seconds to ensure taring is even for all load cells
  tareCells();
}

void loop() {
//  float num = .get_units(10);
  Serial.print("  A:  ");
  Serial.print(cellA.get_units(10), 2);
  Serial.print("  B:  ");
  Serial.print(cellB.get_units(10), 2);
  Serial.print("  C:  ");
  Serial.println(cellC.get_units(10), 2);

  if(Serial.available()>0){
    if(Serial.read()=='T'){
      Serial.println("TARE");
      tareCells();
    }
  }
  
}


void tareCells(){
  cellA.tare();
  cellB.tare();
  cellC.tare();
}
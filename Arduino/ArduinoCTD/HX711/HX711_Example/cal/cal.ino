#include "HX711.h"

HX711 cellA;
HX711 cellB;
HX711 cellC;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 Demo");

  Serial.println("Initializing the scale");
  // parameter "gain" is ommited; the default value 128 is used by the library
  // HX711.DOUT	- pin #A1
  // HX711.PD_SCK	- pin #A0
  cellA.begin(7, 6);
  cellB.begin(5, 4);
  cellC.begin(3, 2);
  cellA.set_scale(450.5f);
  cellB.set_scale(442.f);
  cellC.set_scale(453.f);
  cellA.tare();
  cellB.tare();
  cellC.tare();
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
      Serial.println("tare");
      cellA.tare();
      cellB.tare();
      cellC.tare();
    }
  }
  

}

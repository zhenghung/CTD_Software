#include "HX711.h"

HX711 scale;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 Demo");

  Serial.println("Initializing the scale");
  // parameter "gain" is ommited; the default value 128 is used by the library
  // HX711.DOUT	- pin #A1
  // HX711.PD_SCK	- pin #A0
  scale.begin(A1, A0);
  scale.set_scale();
  scale.tare();
}

void loop() {
  float num = scale.get_units(10);
  Serial.println(scale.get_units(10), 1);
}

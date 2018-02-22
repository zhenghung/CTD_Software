/******************************************************************************
QRD1114_Proximity_Example.ino
Example sketch for SparkFun's QRD1114 Reflectance Proximity Sensor
  (https://www.sparkfun.com/products/246)
Jim Lindblom @ SparkFun Electronics
May 2, 2016

Connect a QRD1114, 330 resistor and 10k resistor as follows:

QRD1114 Pin ---- Arduino ---- Resistors
    1              A0      10k Pull-up to 5V
    2              GND
    3                      330 Resistor to 5V
    4              GND

As an object comes closer to the QRD1114, the voltage on A0 should go down.

Development environment specifics:
Arduino 1.6.7
******************************************************************************/
const int SENSORPIN1 = A1; // Sensor output voltage
const int SENSORPIN2 = A2; // Sensor output voltage

void setup() 
{
  Serial.begin(230400);
  pinMode(SENSORPIN1, INPUT);
  pinMode(SENSORPIN2, INPUT);
}

void loop() 
{
  // Read in the ADC and convert it to a voltage:
  int proximityADC = analogRead(SENSORPIN1);
  float proximityV = (float)proximityADC * 5.0 / 1023.0;
  Serial.println(proximityV);
  
  proximityADC = analogRead(SENSORPIN2);
  proximityV = (float)proximityADC * 5.0 / 1023.0;
  Serial.println(proximityV);
  delay(100);
}

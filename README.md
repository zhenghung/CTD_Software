# CubeSat Testing Device

> Arduino folder contains .ino sketches

> Python folder contains .py files 

**Arduino Libraries Used:**
1. [bodge's HX711 library](https://github.com/bogde/HX711)


**Python Libraries Required:**
1. [Tkinter](https://wiki.python.org/moin/TkInter)
2. [pySerial](https://github.com/pyserial/pyserial)
3. [Matplotlib](https://matplotlib.org/)
4. [numpy](http://www.numpy.org/)

**Calibration Instruction**

Load Cell Calibration
1. Build and upload Calibration.ino sketch onto the arduino UNO
2. Connect the load cell and amplifiers as described in the comments
3. Open the serial monitor and add a known weight onto the load cell
4. If it's not accurate, change the set_scale(value) until it does become accurate
5. This value is calculated by using set_scale() with no parameters, taking the output and dividing it by the known weight
6. Replace the value, performing trial and error till it's accurate and repeat for each load cell

**Build Instructions:**
1. Ensure the required libraries are preinstalled
2. Compile and Upload the ArduinoCTD.ino sketch
3. Build and run the mergedBuild.py file to open the GUI

**EXE build Instructions**
1. cx_Freeze required
2. run ```python setup.py <folderName> ``` in the command line window of the directory
3. Open the build folder created and run mergedBuild.exe

## Operation Instructions
Arduino begins in STARTUP mode and the buttons will switch the states as shown below

### Arduino State Diagram
![StateDiagram with no Calibration](https://github.com/zhenghung/CTD-GUI/blob/master/CTD_StateDiagram.png)

### Circuit Connections 
![Fritzing Diagram](https://github.com/zhenghung/CTD-GUI/blob/master/CTD_SubsystemV2.png)

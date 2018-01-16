""" 2 functions alternating by sending and receiving serial signal to and from Arduino
"""

import serial
import os
first = True
mySerial = serial.Serial('COM3',  9600)

def waitingOn():
	while True:
		bytesToRead=mySerial.inWaiting()
		if(bytesToRead>0):
			myData = mySerial.readline()
			myData=str(myData,'utf-8')
			myData = os.linesep.join([s for s in myData.splitlines() if s])
			if(int(myData.lstrip('Number: '))==20):
				break
			print(myData)
	movingOn()

def movingOn():
	print("We're Done")
	mySerial.write(bytes('A', 'UTF-8'))
	waitingOn()

# print('something')
if first==True:
	first=False
	waitingOn()
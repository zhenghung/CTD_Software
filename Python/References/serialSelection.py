import serial.tools.list_ports
list = serial.tools.list_ports.comports()

comstr = list[0]

print(str(comstr[0]))





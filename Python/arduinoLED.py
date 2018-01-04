import serial
import time
import tkinter

global ser, s, ser_entry_str

def quit():
    global tkTop
    tkTop.destroy()

def setCheckButtonText(varCheckButton):
    if varCheckButton == 'LED ON':
        varLabel.set("LED ON")
        ser.write(bytes('H', 'UTF-8'))
    elif varCheckButton == 'LED Blink':
        varLabel.set("LED Blink")
        ser.write(bytes('B', 'UTF-8'))
    else:
        varLabel.set("LED OFF")
        ser.write(bytes('L', 'UTF-8'))

# def setSerial():
ser = serial.Serial('COM3', 9600)
print("Reset Arduino")
time.sleep(3)
ser.write(bytes('L', 'UTF-8'))





tkTop = tkinter.Tk()
tkTop.geometry('300x200')

frame = tkinter.Frame(tkTop)
frame.pack(side='top')

serialLabel = tkinter.StringVar()
serialLabel.set('COM Port: ')
serLabel = tkinter.Label(frame, textvariable=serialLabel)
serLabel.grid(row = 0, column = 0)

ser_entry_str = tkinter.StringVar()
ser_entry_str.set('COM3')
ser_entry = tkinter.Entry(frame, width=8, textvariable=ser_entry_str)
ser_entry.grid(row = 0, column = 1)

# varSerButton = tkinter.StringVar()
# ser_Button = tkinter.Button(
#     frame, 
#     text="Set", 
#     command=setSerial)
# ser_Button.grid(row = 0, column = 2)

varLabel = tkinter.StringVar()
tkLabel = tkinter.Label(tkTop, textvariable=varLabel)
tkLabel.pack()

varCheckButton = tkinter.StringVar()
# tkCheckButton = tkinter.Checkbutton(
#     tkTop,
#     text="Control Arduino LED",
#     variable=varCheckButton,
#     command=setCheckButtonText)
tkCheckButton = tkinter.OptionMenu(tkTop, varCheckButton, 'LED OFF','LED ON','LED Blink', command = setCheckButtonText)
tkCheckButton.pack()

tkButtonQuit = tkinter.Button(
    tkTop,
    text="Quit",
    command=quit)
tkButtonQuit.pack()

tkinter.mainloop()
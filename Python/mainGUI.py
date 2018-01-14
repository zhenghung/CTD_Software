from tkinter import *
import comWindow
import moiWindow
import calWindow
# -----------------------------------------------------------------------------
# To use matplotlib, the author must use the TkAgg backend, or none of this will
# work and a long string of inexplicable error messages will ensue.
# -----------------------------------------------------------------------------
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import serial

global serialConnect, cs_config, ser
ser = 0

# Define a bold font:
BOLD = ('Helvetica', '24', 'bold')

# Create main application window.
root = Tk()
root.title('CubeSat Testing Device')

# Create a text box explaining the application.
greeting = Label(text="CubeSat Testing Device", font=BOLD)
greeting.pack(side='top')

# Create a frame for variable names and entry boxes for their values.
frametop = Frame(root)
frametop.pack(side='top')
frame = Frame(frametop)
frame.pack(side='left')
frame2 = Frame(frametop)
frame2.pack(side='right')
frame21 = Frame(frame2)
frame21.pack(side='top')



# Variables for the calculation, and default values.
row_counter = 0

# Connect to Arduino
def serialConnect(event=None):
    global ser
    try:
        ser = serial.Serial('COM3', 9600)
        connect = Label(frame, text="Success", font='Calibri 12 bold', fg='green')
        connect.grid(row=0, column=1)
    except serial.SerialException: 
        connect = Label(frame, text="Failed", font='Calibri 12 bold', fg='Red')
        connect.grid(row=0, column=1)



# Arduino Button
arduino = Button(frame, command=serialConnect, text="Connect to Arduino")
arduino.grid(row=row_counter, column=0, padx=5)

row_counter+=1
cs_text = Label(frame, text='CubeSat Config:')
cs_text.grid(row=row_counter, column=0)

cs_config = StringVar(root)
cs_config.set("3U") # default value

w = OptionMenu(frame, cs_config, "1U", "2U", "3U")
w.grid(row = row_counter, column = 1)


ins_text = Label(frame21, text='1. Place the CubeSat onto the platform with the predefined orientation\n'
                               '2. Ensure the fixturing is properly clamping the CubeSat\n'
                               '3. Select the appropriate config and Mode of operation', justify = 'left')
ins_text.grid(row = 0, column = 0, padx=10)


# Calibration Mode
def cal_mode(event=None):
    global cellA, cellB, cellC, timer
    calWindow.calMode.cal_start(ser, cs_config)

# Calibration Button
Mode_COM = Button(root, command = cal_mode, text="Calibrate Measurements")
Mode_COM.pack(side='top', fill='both', padx=5, pady=2)

# Notebook TabsView
from tkinter import ttk
tabsView = ttk.Notebook(root)
comFrame = Frame(tabsView)
moiFrame = Frame(tabsView)
tabsView.add(comFrame, text='Center of Mass')
tabsView.add(moiFrame, text='Moment of Inertia')
tabsView.pack(side='top', fill='both', padx=5, pady=5)

# Setup COM and MOI Mode
comWindow.comMode.com_start(ser, cs_config, comFrame)
moiWindow.moi_start(ser, cs_config, moiFrame)


# Allow pressing <Esc> to close the window.
root.bind('<Escape>', lambda e: root.quit())

# The window is not resizable. 
root.resizable(0,0) 

# Activate the window.
root.mainloop()



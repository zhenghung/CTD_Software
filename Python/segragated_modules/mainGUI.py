from tkinter import *

import time
import serial
import calWindow
from moiWindow import moiMode
from comWindow import comMode

ser = 0
BOLD = ('Helvetica', '24', 'bold')
default_cs = '3U'
# Button Functions
# --------------------------
# Connect to Arduino
def serialConnect():
    global ser
    try:
        ser = serial.Serial('COM3', 9600)
        connect = Label(controlFrame, text="Success", font='Calibri 12 bold', fg='green')
        connect.grid(row=0, column=1)
        ser.close()
        ser.open()
        time.sleep(2)  #at least wait for 2s 
    except serial.SerialException: 
        connect = Label(controlFrame, text="Failed", font='Calibri 12 bold', fg='Red')
        connect.grid(row=0, column=1)

# Calibration Mode
def cal_mode():
    global cellA, cellB, cellC, timer
    calWindow.calMode.cal_start(ser, cs_config)

# ---------------------------

class mainGUI(object):
    def  __init__(self):
        from tkinter import ttk
        global cs_config, ser, mainStatus, controlFrame
        # Create main application window.
        root = Tk()
        root.title('CubeSat Testing Device')

        # Frame Containers
        titleFrame = Frame(root)
        titleFrame.grid(row=0)
        mainUIFrame = Frame(root, borderwidth=3, relief=GROOVE)
        mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)
        tabFrame = Frame(root)
        tabFrame.grid(row=2)

        # SubFrame Containers
        controlFrame = Frame(mainUIFrame, borderwidth=3, relief=GROOVE)
        controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
        instructionFrame = Frame(mainUIFrame, borderwidth=3, relief=GROOVE)
        instructionFrame.grid(row=0, column=1, sticky='nsew', padx=(10, 10))
        stsFrame = Frame(mainUIFrame, borderwidth=3, relief=GROOVE)
        stsFrame.grid(row=0, column=2, sticky='nsew', padx=10)

        # Title
        titleLabel = Label(titleFrame, text="CubeSat Testing Device", font=BOLD)
        titleLabel.grid(row=0)

        # Arduino Button
        arduino = ttk.Button(controlFrame, command=serialConnect, text="Connect to Arduino")
        arduino.grid(row=0, column=0, padx=5, sticky='nsew')


        # CubeSat Config selection
        cs_text = Label(controlFrame, text='CubeSat Config:')
        cs_text.grid(row=1, column=0)
        cs_config = StringVar(root)
        cs_config.set(default_cs)
        w = ttk.OptionMenu(controlFrame, cs_config, '', "1U", "2U", "3U")
        w.grid(row = 1, column = 1, sticky='nsew')

        # Calibration Button
        calButton = ttk.Button(controlFrame, command = cal_mode, text="Calibrate Measurements")
        calButton.grid(row=2, columnspan=2, sticky='nsew')

        # Instructions Label
        ins_text = Label(instructionFrame, text=
            '1. Place the CubeSat onto the platform with the predefined orientation\n'
            '2. Ensure the fixturing is properly clamping the CubeSat\n'
            '3. Select the appropriate config and Mode of operation\n'
            '4. Calibrate Measurements with the specified block for first time measurements'
            , justify = 'left')
        ins_text.config(width=60)
        ins_text.grid(row = 0, column = 0, padx=5, sticky='nsew')

        #Status Label
        stslbl = Label(stsFrame, text='Arduino State')
        stslbl.grid(row=0, padx=10, pady=(5,0), sticky='nw')
        mainStatus = StringVar(root)
        mainStatus.set('Center of Mass Mode')
        status_label = Label(stsFrame, textvariable=mainStatus, justify='left', anchor=NW, font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
        status_label.config(height = 2, width=50, wraplength=320)
        status_label.grid(row=1, padx=10, pady=(0,5), sticky='nsew')

        # Notebook TabsView
        from tkinter import ttk
        tabsView = ttk.Notebook(tabFrame)
        comFrame = Frame(tabsView)
        moiFrame = Frame(tabsView)
        tabsView.add(comFrame, text='Center of Mass')
        tabsView.add(moiFrame, text='Moment of Inertia')
        tabsView.pack(side='top', fill='both', padx=0, pady=5)

        # Setup COM and MOI Mode
        comMode.com_start(ser, cs_config, mainStatus, comFrame)
        moiMode.moi_start(ser, cs_config, mainStatus, moiFrame)

        # Allow pressing <Esc> to close the window.
        root.bind('<Escape>', lambda e: root.quit())

        # The window is not resizable. 
        root.resizable(0,0) 

        # print ('height:',root.winfo_height())
        # print ('width:',root.winfo_width())

        # Activate the window.
        root.mainloop()


if __name__=='__main__':
    mainGUI()

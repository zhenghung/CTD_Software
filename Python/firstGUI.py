try:
    # This will work in Python 2.7
    import Tkinter
except ImportError:
    # This will work in Python 3.5
    import tkinter as Tkinter


import comWindow as myCOM
# -----------------------------------------------------------------------------
# To use matplotlib, the author must use the TkAgg backend, or none of this will
# work and a long string of inexplicable error messages will ensue.
# -----------------------------------------------------------------------------
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import serial

global ser, cs_config
cs_config='3U'
# Define a bold font:
BOLD = ('Helvetica', '24', 'bold')

# Create main application window.
root = Tkinter.Tk()

# Create a text box explaining the application.
greeting = Tkinter.Label(text="CubeSat Testing Device", font=BOLD)
greeting.pack(side='top')

# Create a frame for variable names and entry boxes for their values.
frametop = Tkinter.Frame(root)
frametop.pack(side='top')
frame = Tkinter.Frame(frametop)
frame.pack(side='left')
frame2 = Tkinter.Frame(frametop)
frame2.pack(side='right')
frame21 = Tkinter.Frame(frame2)
frame21.pack(side='top')









# Variables for the calculation, and default values.
amplitudeA = Tkinter.StringVar()
amplitudeA.set('1.0')
frequencyA = Tkinter.StringVar()
frequencyA.set('1.0')

amplitudeB = Tkinter.StringVar()
amplitudeB.set('1.0')
frequencyB = Tkinter.StringVar()
frequencyB.set('1.0')

deltaPhi = Tkinter.StringVar()
deltaPhi.set('0.0')
row_counter = 0

# Connect to Arduino
def serialConnect(event=None):
    try:
        ser = serial.Serial('COM3', 9600)
        connect = Tkinter.Label(frame, text="Success", font='Calibri 12 bold', fg='green')
        connect.grid(row=0, column=1)
    except serial.SerialException: 
        connect = Tkinter.Label(frame, text="Failed", font='Calibri 12 bold', fg='Red')
        connect.grid(row=0, column=1)




# Arduino Button
arduino = Tkinter.Button(frame, command=serialConnect, text="Connect to Arduino")
arduino.grid(row=row_counter, column=0)

# Create text boxes and entry boxes for the variables.
# Use grid geometry manager instead of packing the entries in.

row_counter+=1
cs_text = Tkinter.Label(frame, text='CubeSat Config:')
cs_text.grid(row=row_counter, column=0)

variable = Tkinter.StringVar(root)
variable.set("3U") # default value

w = Tkinter.OptionMenu(frame, variable, "1U", "2U", "3U")
w.grid(row = row_counter, column = 1)


ins_text = Tkinter.Label(frame21, text='1. Place the CubeSat onto the platform with the predefined orientation\n'
                                       '2. Ensure the fixturing is properly clamping the CubeSat\n'
                                       '3. Select the appropriate config and Mode of operation\n', justify = 'left')
ins_text.grid(row = 0, column = 0)




#
# row_counter += 1
# aa_text = Tkinter.Label(frame, text='Amplitude of 1st wave:')
# aa_text.grid(row=row_counter, column=0)
#
# aa_entry = Tkinter.Entry(frame, width=8, textvariable=amplitudeA)
# aa_entry.grid(row=row_counter, column=1)
#
# row_counter += 1
# fa_text = Tkinter.Label(frame, text='Frequency of 1st wave:')
# fa_text.grid(row=row_counter, column=0)
#
# fa_entry = Tkinter.Entry(frame, width=8, textvariable=frequencyA)
# fa_entry.grid(row=row_counter, column=1)
#
# row_counter += 1
# ab_text = Tkinter.Label(frame, text='Amplitude of 2nd wave:')
# ab_text.grid(row=row_counter, column=0)
#
# ab_entry = Tkinter.Entry(frame, width=8, textvariable=amplitudeB)
# ab_entry.grid(row=row_counter, column=1)
#
# row_counter += 1
# fb_text = Tkinter.Label(frame, text='Frequency of 2nd wave:')
# fb_text.grid(row=row_counter, column=0)
#
# fb_entry = Tkinter.Entry(frame, width=8, textvariable=frequencyB)
# fb_entry.grid(row=row_counter, column=1)
#
# row_counter += 1
# dp_text = Tkinter.Label(frame, text='Phase Difference:')
# dp_text.grid(row=row_counter, column=0)
#
# dp_entry = Tkinter.Entry(frame, width=8, textvariable=deltaPhi)
# dp_entry.grid(row=row_counter, column=1)





# Define a function to create the desired plot.
def make_plot(event=None):
    # Get these variables from outside the function, and update them.
    global amplitudeA, frequencyA, amplitudeB, frequencyB, deltaPhi

    # Convert StringVar data to numerical data.
    aa = float(amplitudeA.get())
    fa = float(frequencyA.get())
    ab = float(amplitudeB.get())
    fb = float(frequencyB.get())
    phi = float(deltaPhi.get())

    # Define the range of the plot.
    t_min = -10
    t_max = 10
    dt = 0.01
    t = np.arange(t_min, t_max+dt, dt)

    # Create the two waves and find the combined intensity.
    waveA = aa * np.cos(fa * t)
    waveB = ab * np.cos(fb * t + phi)
    intensity = (waveA + waveB)**2

    # Create the plot.
    plt.figure()
    plt.plot(t, intensity, lw=3)
    plt.title('Interference Pattern')
    plt.xlabel('Time')
    plt.ylabel('Intensity')
    plt.show()


# Add a button to create the plot.
MakePlot = Tkinter.Button(frame2, command=make_plot, text="Create Plot")
MakePlot.pack(side='bottom', fill='both')




# COM Mode
def com_mode(event=None):
    global cellA, cellB, cellC
    myCOM.com_start(cs_config)


# COM Button
Mode_COM = Tkinter.Button(root, command = com_mode, text="Measure Center of Mass")
Mode_COM.pack(side='top', fill='both')

# MOI Mode
def moi_mode(event=None):
    global timer
    moi_window = Tkinter.Toplevel(root)
    moi_frame = Tkinter.Frame(moi_window)
    moi_label = Tkinter.Label(moi_window, text="Moment of Inertia Mode", font='Helvetica 16 bold')
    moi_label.pack(side='top')

# MOI Button
Mode_MOI = Tkinter.Button(root, command = moi_mode, text="Measure Moment of Inertia")
Mode_MOI.pack(side='top', fill='both')

# Calibration Mode
def cal_mode(event=None):
    global cellA, cellB, cellC, timer
    cal_window = Tkinter.Toplevel(root)
    cal_frame = Tkinter.Frame(cal_window)
    cal_label = Tkinter.Label(cal_window, text="Calibration Mode", font='Helvetica 16 bold')
    cal_label.pack(side='top')

# Calibration Button
Mode_COM = Tkinter.Button(root, command = cal_mode, text="Calibrate Measurements")
Mode_COM.pack(side='top', fill='both')







# Allow pressing <Return> to create plot.
root.bind('<Return>', make_plot)

# Allow pressing <Esc> to close the window.
root.bind('<Escape>', root.destroy)

# Activate the window.
root.mainloop()
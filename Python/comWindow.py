import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
import serial

global cs_config, ser

def com_start(ser, cs_config):
	global status_str
	if ser==0:
		cs_config = cs_config.get()
	# Setup Window
	com_window = Tk()
	com_window.title("COM Mode")
	# com_window.geometry('300x200')
	com_label = Label(com_window, text="Centre of Mass Mode", font='Helvetica 16 bold')
	com_label.pack(side='top')

	# Frame 1
	com_frame1 = Frame(com_window)
	com_frame1.pack(side='left')
	com_frame2 = Frame(com_window)
	com_frame2.pack(side='right')
	com_frame3 = Frame(com_window)
	com_frame3.pack(side='bottom')

	# CubeSat Mode Label		
	cs_label = Label(
		com_frame1, 
		text='CubeSat Mode: '+cs_config+'\n\n'
		'1. Place the CubeSat on the plate in orientation 1\n'
		'2. Begin measurement for orientation 1\n'
		'3. Wait for measurement to complete\n'
		'4. Reorientate and fix CubeSat in orientation 2\n'
		'5. Begin measurement for orientation 2\n'
		'6. Wait for measurement to complete\n'
		'7. Reorientate and fix CubeSat in orientation 3\n'
		'8. Begin measurement for orientation 3\n'
		'9. Wait for measurement to complete\n'
		'10. Click finish to obtain final COM\n\n'
		'Status Message: ',justify='left')
	cs_label.pack(padx=10)

	#Status Label
	status_str = StringVar(com_window)
	status_str.set('Place CubeSat to begin')
	status_label = Label(com_frame1, textvariable=status_str, justify='left', anchor=NW, font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
	status_label.config(height=3, width=30, wraplength=240)
	status_label.pack(padx=10, pady=10)

	measureButton1 = Button(com_frame1,text='Orientation 1 Measure', command=measure1)
	measureButton1.pack(fill=X)
	measureButton2 = Button(com_frame1,text='Orientation 2 Measure', command=measure2)
	measureButton2.pack(fill=X)
	measureButton3 = Button(com_frame1,text='Orientation 3 Measure', command=measure3)
	measureButton3.pack(fill=X)
	finishButton = Button(com_frame1,text='Compute Measurements', command=finish)
	finishButton.pack(fill=X)


	# Activate the window.
	com_window.mainloop()     

def measure1():
	status_str.set('Measuring Orientation 1...')

def measure2():
	status_str.set('Measuring Orientation 2...')

def measure3():
	status_str.set('Measuring Orientation 3...')

def finish():
	status_str.set('Computing Results...')


com_start(1, '3U')


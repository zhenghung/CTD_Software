import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
import serial

global cs_config, ser

def moi_start(ser, cs_config, moi_window):
	global status_str
	if ser==0:
		cs_config = cs_config.get()

	# Setup Window
	# moi_window = Tk()
	# moi_window.title("MOI Mode")
	# moi_window.geometry('300x200')
	moi_label = Label(moi_window, text="Moment of Inertia Mode", font='Helvetica 16 bold')
	moi_label.pack(side='top')

	# Frame 1
	moi_frame1 = Frame(moi_window)
	moi_frame1.pack(side='left')
	moi_frame2 = Frame(moi_window)
	moi_frame2.pack(side='right')
	moi_frame3 = Frame(moi_window)
	moi_frame3.pack(side='bottom')

	# CubeSat Mode Label		
	cs_label = Label(
		moi_frame1, 
		text='Instructions: \n\n'
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
	status_str = StringVar(moi_window)
	status_str.set('Place CubeSat to begin')
	status_label = Label(moi_frame1, textvariable=status_str, justify='left', anchor=NW, font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
	status_label.config(height=3, width=30, wraplength=240)
	status_label.pack(padx=10, pady=10)

	measureButton1 = Button(moi_frame1,text='Orientation 1 Measure', command=measure1)
	measureButton1.pack(fill='both')
	measureButton2 = Button(moi_frame1,text='Orientation 2 Measure', command=measure2)
	measureButton2.pack(fill=X)
	measureButton3 = Button(moi_frame1,text='Orientation 3 Measure', command=measure3)
	measureButton3.pack(fill=X)
	finishButton = Button(moi_frame1,text='Compute Measurements', command=finish)
	finishButton.pack(fill=X)


	# Activate the window.
	if ser==1:
		moi_window.mainloop()     

def measure1():
	status_str.set('Rotate plate to begin measurement 1')

def measure2():
	status_str.set('Rotate plate to begin measurement 2')

def measure3():
	status_str.set('Rotate plate to begin measurement 3')

def finish():
	status_str.set('Computing Results...')

moi_window = Tk()
moi_start(1, '3U', moi_window)

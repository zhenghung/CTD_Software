import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
import tkinter
import serial

global cs_config, ser

def com_start(ser, cs_config):
	global status_str
	cs_config = cs_config.get()
	# Setup Window
	com_window = tkinter.Tk()
	com_window.title("COM Mode")
	# com_window.geometry('300x200')
	com_label = tkinter.Label(com_window, text="Centre of Mass Mode", font='Helvetica 16 bold')
	com_label.pack(side='top')

	# Frame 1
	com_frame1 = tkinter.Frame(com_window)
	com_frame1.pack(side='left')
	com_frame2 = tkinter.Frame(com_window)
	com_frame2.pack(side='right')
	com_frame3 = tkinter.Frame(com_window)
	com_frame3.pack(side='bottom')

	# CubeSat Mode Label		
	cs_label = tkinter.Label(
		com_frame1, 
		text='CubeSat Mode: '+cs_config+'\n\n'
		'1. Place the CubeSat on the plate in orientation 1\n'
		'2. Begin measurement for orientation 1\n'
		'3. Wait for measurement to complete\n'
		'4. Reorientate and fix CubeSat in orientation 2\n'
		'5. Begin measurement for orientation 2\n'
		'6. Wait for measurement to complete\n'
		'6. Reorientate and fix CubeSat in orientation 3\n'
		'7. Begin measurement for orientation 3\n'
		'8. Wait for measurement to complete\n'
		'9. Click finish to obtain final COM\n\n'
		'Status Message: ',justify='left')
	cs_label.pack(padx=10)

	#Status Label
	status_str = tkinter.StringVar(com_window)
	status_str.set('Place CubeSat to begin')
	status_label = tkinter.Label(com_frame1, textvariable=status_str, justify='left', font='i', fg='gray')
	status_label.pack(pady=10)

	measureButton1 = tkinter.Button(com_frame1,text='Orientation 1 Measure', command=measure1)
	measureButton1.pack(fill=tkinter.X)
	measureButton2 = tkinter.Button(com_frame1,text='Orientation 2 Measure', command=measure2)
	measureButton2.pack(fill=tkinter.X)
	measureButton3 = tkinter.Button(com_frame1,text='Orientation 3 Measure', command=measure3)
	measureButton3.pack(fill=tkinter.X)
	finishButton = tkinter.Button(com_frame1,text='Compute Measurements', command=finish)
	finishButton.pack(fill=tkinter.X)


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


# com_start(1, '3U')


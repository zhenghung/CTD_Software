import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
import serial
from tkinter import messagebox
from tkinter import ttk
# import mainGUI

global cs_config, ser

class moiMode():

	def moi_start(ser, cs_config, parentStatus, moi_window):
		global status_str, result_str, mainStatus
		if ser==0:
			cs_config = cs_config.get()
		mainStatus = parentStatus
		# Setup Window
		# moi_window = Tk()
		# moi_window.title("MOI Mode")
		# moi_window.geometry('300x200')

		# Frame Containers
		titleFrame = Frame(moi_window)
		titleFrame.grid(row=0, column=0)	
		mainUIFrame = Frame(moi_window, borderwidth=3, relief=GROOVE)
		mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		# SubFrame Containers
		controlFrame = Frame(mainUIFrame, borderwidth=0, relief=GROOVE)
		controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		resultFrame = Frame(mainUIFrame, borderwidth=0, relief=GROOVE)
		resultFrame.grid(row=0, column=1, sticky='nsew', padx=10)

		# Frames
		instructionFrame = Frame(controlFrame, borderwidth=3, relief=GROOVE)
		instructionFrame.grid(row=0, sticky='nsew', padx=10)
		buttonFrame = Frame(controlFrame, borderwidth=3, relief=GROOVE)
		buttonFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		stsFrame = Frame(controlFrame, borderwidth=3, relief=GROOVE)
		stsFrame.grid(row=2, column=0, sticky='sew', padx=10) 
		graphFrame = Frame(resultFrame, borderwidth=3, relief=GROOVE)
		graphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		printFrame = Frame(resultFrame, borderwidth=3, relief=GROOVE)
		printFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		moi_label = Label(titleFrame, text="Moment of Inertia Mode", font='Helvetica 16 bold')
		moi_label.pack(side='top')

		# Arduino MOI Standby button
		moiStand = ttk.Button(instructionFrame, text='MOI Standby', command=moiMode.standby)
		moiStand.pack(padx=10, pady=2, fill=X)	

		# Reset Button
		resetButton = ttk.Button(instructionFrame, text='Reset', command=moiMode.reset)
		resetButton.pack(padx=10, pady=2, fill='both')

		# MOI Mode Instruction	
		cs_label = Label(
			instructionFrame, 
			text='Instructions: \n\n'
			'1. Place the CubeSat on the plate in orientation 1\n'
			'2. Switch to Arduino COM Standby Mode\n'
			'3. Begin measurement for orientation 1\n'
			'4. Wait for measurement to complete\n'
			'5. Reorientate and fix CubeSat in orientation 2\n'
			'6. Begin measurement for orientation 2\n'
			'7. Wait for measurement to complete\n'
			'8. Reorientate and fix CubeSat in orientation 3\n'
			'9. Begin measurement for orientation 3\n'
			'10. Wait for measurement to complete\n'
			'11. Click finish to obtain final COM\n',justify='left')
		cs_label.pack(padx=10)

		#Status Label
		stslbl = Label(stsFrame, text='Status Message')
		stslbl.grid(row=0, padx=10, pady=5, sticky='nw')
		status_str = StringVar(moi_window)
		status_str.set('Place CubeSat to begin')
		status_label = Label(stsFrame, textvariable=status_str, justify='left', anchor=NW, font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=16, width=40, wraplength=320)
		status_label.grid(row=1, padx=10, pady=5)	

		# Buttons Layout
		measureButton1 = ttk.Button(buttonFrame,text='Orientation 1 Measure', command=moiMode.measure1)
		measureButton1.pack(fill=X)
		measureButton2 = ttk.Button(buttonFrame,text='Orientation 2 Measure', command=moiMode.measure2)
		measureButton2.pack(fill=X)
		measureButton3 = ttk.Button(buttonFrame,text='Orientation 3 Measure', command=moiMode.measure3)
		measureButton3.pack(fill=X)
		finishButton = ttk.Button(buttonFrame,text='Compute Measurements', command=moiMode.finish)
		finishButton.pack(fill=X)

		# Plot Graph
		moiMode.plot(graphFrame)

		# Results Textbox
		resultlbl = Label(printFrame, text='Results')
		resultlbl.grid(row=0, padx=10, pady=5, sticky='nw')
		result_str = StringVar(moi_window)
		result_str.set('Results to be printed HERE...')
		result_label = Label(printFrame, textvariable=result_str, justify='left', anchor=NW, font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=10, width=80, wraplength=640)
		result_label.grid(row=1, padx=10, pady=5)


		# Activate the window.
		if ser==1:
			moi_window.mainloop()     

	def standby():
		mainStatus.set('State MOI')
		status_str.set('Arduino: MOI Standby Mode\nAwaiting further instructions')

	def reset():
	    result = messagebox.askyesno("Reset?", "Are You Sure?\nAll data will be lost", icon='warning')
	    if result == True:
	        status_str.set('Reset Success\nPlace CubeSat to begin...')
		
	def measure1():
		mainStatus.set('State MOI Measure 1')
		status_str.set('Rotate plate to begin measurement 1')

	def measure2():
		status_str.set('Rotate plate to begin measurement 2')

	def measure3():
		status_str.set('Rotate plate to begin measurement 3')

	def finish():
		status_str.set('Computing Results...')

	def plot(graphFrame):
		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
		import matplotlib.backends.backend_tkagg as tkagg
		from matplotlib.figure import Figure

		fig = Figure()
		ax = fig.add_subplot(111)
		line, = ax.plot(range(10))

		canvas = FigureCanvasTkAgg(fig,master=graphFrame)
		canvas.show()
		canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

		# canvas is your canvas, and root is your parent (Frame, TopLevel, Tk instance etc.)
		tkagg.NavigationToolbar2TkAgg(canvas, graphFrame)
		# ax.mouse_init()


# moi_window = Tk()
# moiMode.moi_start(1, '3U', moi_window)

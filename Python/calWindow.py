import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
from tkinter import ttk
import serial

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt



global cs_config, ser
class calMode():
	def __init__():
		self.cal_start(ser, cs_config)

	def cal_start(ser, cs_config):
		global status_str, calType_str, cal_window
		if ser==0:
			cs_config = cs_config.get()

		# Setup Window
		cal_window = Tk()
		cal_window.title("CAL Mode")
		# cal_window.geometry('300x200')

		# Frame Containers
		titleFrame = Frame(cal_window)
		titleFrame.grid(row=0, column=0)	
		stsFrame = Frame(cal_window, borderwidth=3, relief=GROOVE)
		stsFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		mainUIFrame = Frame(cal_window, borderwidth=3, relief=GROOVE)
		mainUIFrame.grid(row=2, column=0, sticky='nsew', padx=10)
		comFrame = Frame(cal_window, borderwidth=3, relief=GROOVE)	
		comFrame.grid(row = 3, column = 0, sticky = 'nsew', padx = 10)
		moiFrame = Frame(cal_window, borderwidth=3, relief=GROOVE)
		moiFrame.grid(row = 4, column = 0, sticky = 'nsew', padx = 10)

		# Frames within mainUIFrame Containers
		calOptionFrame = Frame(mainUIFrame)
		calOptionFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		insFrame = Frame(mainUIFrame)
		insFrame.grid(row = 0, column = 1, sticky ='nsew', padx = 10)

		# Frames within comFrame Container
		comFrameUI = Frame(comFrame)
		comFrameUI.grid(row = 0, column = 0, sticky = 'nsew', padx =10)
		graphFrame = Frame(comFrame, borderwidth=3, relief=GROOVE)
		graphFrame.grid(row = 0, column = 1, sticky = 'e', padx=10)

		# Frames within moiFrame Container


		# layout all of the main containers
		cal_window.grid_rowconfigure(1, weight=1)
		cal_window.grid_columnconfigure(0, weight=1)

		# Title Label
		cal_label = Label(titleFrame, text="Calibration Mode", font='Helvetica 16 bold')
		cal_label.grid(row=0, column=0)

		# Status Window
		sts_label = Label(stsFrame, text='Status Message: ', justify='left')
		sts_label.grid(row=0,column=0, sticky='w')
		status_str = StringVar(cal_window)
		status_str.set('Place Calibration Block to begin')
		status_label = Label(stsFrame, textvariable=status_str, justify='left', anchor=NW, font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=3, width=100, wraplength=640)
		status_label.grid(row=1, column=0, sticky='nw', pady=10, padx=5)
		print(stsFrame.winfo_width())

		# OptionMenu
		calType_str = StringVar(cal_window)
		calType_str.set('COM')
		calTypeLbl = Label(calOptionFrame, text='Calibration Type: ')
		calTypeLbl.grid(row = 0, column = 0, sticky = 'w')
		calType = ttk.OptionMenu(calOptionFrame, calType_str, "","MOI", "COM")
		calType.grid(row = 0, column = 1)
		
		# Instruction Labels
		insLabel = Label(
			insFrame, 
			text=
			'1. Place CubeSat on the plate\n'
			'2. Select the Calibration type and Begin calibration measurement'
			, justify='left')	
		insLabel.grid(row = 0, column = 3, sticky='w')


		# COM Section
		calMode.plotCube(graphFrame)
		comlbl = Label(comFrameUI, text='Center of Mass')
		comlbl.grid(row=0, column=0)


		# MOI Section
		moilbl = Label(moiFrame, text='Moment of Inertia')
		moilbl.grid(row=0, column=0)



		saveButton = ttk.Button(cal_window, text='Save and Quit', command=calMode.save)
		saveButton.grid(row=5, column=0, sticky='nse', padx=10, pady=10)

		# The window is not resizable. 
		cal_window.resizable(0,0) 

		# Activate the window.
		cal_window.mainloop()


	def plotCube(graphFrame):
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt
		import numpy as np
		from itertools import product, combinations

		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")

		cubeWidth = 15;

		# draw cube
		r = [0, cubeWidth]
		for s, e in combinations(np.array(list(product(r, r, r))), 2):
		    if np.sum(np.abs(s-e)) == r[1]-r[0]:
		        ax.plot3D(*zip(s, e), color="b")

	    # draw a point
		ax.scatter([cubeWidth/2], [cubeWidth/2], [cubeWidth/2], color="r", s=3)

		canvas = FigureCanvasTkAgg(fig, master=graphFrame)
		canvas.show()
		canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

		ax.mouse_init()


	def save():
		cal_window.destroy()

# calMode.cal_start(1, 'COM')
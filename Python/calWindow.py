import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
import serial

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt



global cs_config, ser

def cal_start(ser, cs_config):
	global status_str, calType_str
	if ser==0:
		cs_config = cs_config.get()

	# Setup Window
	cal_window = Tk()
	cal_window.title("CAL Mode")
	# cal_window.geometry('300x200')

	# Frame Containers
	titleFrame = Frame(cal_window)
	titleFrame.grid(row=0, column=0)	
	stsFrame = Frame(cal_window)
	stsFrame.grid(row=1, column=0, sticky='nw', padx=10)
	mainUIFrame = Frame(cal_window)
	mainUIFrame.grid(row=2, column=0, sticky='w', padx=10)
	calOptionFrame = Frame(mainUIFrame)
	calOptionFrame.grid(row=0, column=0, sticky='w', padx=10)
	insFrame = Frame(mainUIFrame)
	insFrame.grid(row = 0, column = 1, sticky ='w', padx = 10)
	graphFrame = Frame(cal_window)
	graphFrame.grid(row = 3, column = 0, sticky = 'w', padx =10)

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
	status_label.config(height=3, width=80, wraplength=640)
	status_label.grid(row=1, column=0, sticky='nw', pady=10)

	# OptionMenu
	calType_str = StringVar(cal_window)
	calType_str.set('COM')
	calTypeLbl = Label(calOptionFrame, text='Calibration Type: ')
	calTypeLbl.grid(row = 0, column = 0, sticky = 'w')
	calType = OptionMenu(calOptionFrame, calType_str, "MOI", "COM")
	calType.grid(row = 0, column = 1)
	
	# Instruction Labels
	insLabel = Label(
		insFrame, 
		text='1. Place CubeSat on the plate\n'
		'2. Select the Calibration type and Begin calibration measurement', justify='left')	
	insLabel.grid(row = 0, column =3, sticky='w')

	plotCube(graphFrame)


	# Activate the window.
	cal_window.mainloop()

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

def plotCube(graphFrame):




	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.set_aspect("equal")


	# draw cube
	r = [0, 15]
	for s, e in combinations(np.array(list(product(r, r, r))), 2):
	    if np.sum(np.abs(s-e)) == r[1]-r[0]:
	        ax.plot3D(*zip(s, e), color="b")

	canvas = FigureCanvasTkAgg(fig,master=graphFrame)
	canvas.show()
	canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
	ax.mouse_init()


cal_start(1, 'COM')
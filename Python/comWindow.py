import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
from tkinter import messagebox
import serial
from References import PlotCuboid

global cs_config, ser

class comMode():

	def com_start(ser, cs_config, parentStatus, com_window):
		global status_str, result_str, mainStatus
		if ser==0:
			cs_config = cs_config.get()
		mainStatus = parentStatus

		# Setup Window
		# com_window = Tk()
		# com_window.title("COM Mode")
		# com_window.geometry('300x200')

		# Frame Containers
		titleFrame = Frame(com_window)
		titleFrame.grid(row=0, column=0)	
		mainUIFrame = Frame(com_window, borderwidth=3, relief=GROOVE)
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

		com_label = Label(titleFrame, text="Centre of Mass Mode", font='Helvetica 16 bold')
		com_label.pack(side='top')


		# Arduino COM Standby button
		comStand = Button(instructionFrame, text='COM Standby', command=comMode.standby)
		comStand.pack(padx=10, pady=2, fill=X)	

		# Reset Button
		resetButton = Button(instructionFrame, text='Reset', command=comMode.reset)
		resetButton.pack(padx=10, pady=2, fill='both')

		# COM Instructions		
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
			'8. Compute Measurements to obtain final COM\n\n'
			,justify='left')
		cs_label.pack(padx=10, pady=10)

		#Status Label
		stslbl = Label(stsFrame, text='Status Message')
		stslbl.grid(row=0, padx=10, pady=5, sticky='nw')
		status_str = StringVar(com_window)
		status_str.set('Place CubeSat to begin')
		status_label = Label(stsFrame, textvariable=status_str, justify='left', anchor=NW, font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=18, width=40, wraplength=320)
		status_label.grid(row=1, padx=10, pady=5)

		measureButton1 = Button(buttonFrame,text='Orientation 1 Measure', command=comMode.measure1)
		measureButton1.pack(fill=X)
		measureButton2 = Button(buttonFrame,text='Orientation 2 Measure', command=comMode.measure2)
		measureButton2.pack(fill=X)

		finishButton = Button(buttonFrame,text='Compute Measurements', command=comMode.finish)
		finishButton.pack(fill=X)

		# Plot Center of Mass on 3D axes
		comMode.graphPlot(graphFrame)
		# comMode.plot_cuboid(graphFrame, [0, 0, 0], (30 ,10 , 10))


		# Results Textbox
		resultlbl = Label(printFrame, text='Results')
		resultlbl.grid(row=0, padx=10, pady=5, sticky='nw')
		result_str = StringVar(com_window)
		result_str.set('Results to be printed HERE...')
		result_label = Label(printFrame, textvariable=result_str, justify='left', anchor=NW, font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=10, width=80, wraplength=640)
		result_label.grid(row=1, padx=10, pady=5)


		# Activate the window.
		if ser==1:
			com_window.mainloop() 

	def standby():
		mainStatus.set('COM State')			
		status_str.set('Arduino: COM Standby Mode\nAwaiting further instructions')

	def reset():
	    result = messagebox.askyesno("Reset?", "Are You Sure?\nAll data will be lost", icon='warning')
	    if result == True:
	        status_str.set('Reset Success\nPlace CubeSat to begin...')

	def measure1():
		mainStatus.set('COM Measure State')	
		status_str.set('Measuring Orientation 1...')

	def measure2():
		status_str.set('Measuring Orientation 2...')

	def finish():
		status_str.set('Computing Results...')

	def graphPlot(graphFrame):
		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
		from matplotlib.figure import Figure
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt
		import numpy as np
		from itertools import product, combinations
		import matplotlib.backends.backend_tkagg as tkagg
		
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

		tkagg.NavigationToolbar2TkAgg(canvas, graphFrame)
		ax.mouse_init()

	def plot_cuboid(graphFrame, center, size):
		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
		from matplotlib.figure import Figure
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt
		import numpy as np
		from itertools import product, combinations

		ox, oy, oz = center
		l, w, h = size

		x = np.linspace(ox-l/2,ox+l/2,num=10)
		y = np.linspace(oy-w/2,oy+w/2,num=10)
		z = np.linspace(oz-h/2,oz+h/2,num=10)
		x1, z1 = np.meshgrid(x, z)
		y11 = np.ones_like(x1)*(oy-w/2)
		y12 = np.ones_like(x1)*(oy+w/2)
		x2, y2 = np.meshgrid(x, y)
		z21 = np.ones_like(x2)*(oz-h/2)
		z22 = np.ones_like(x2)*(oz+h/2)
		y3, z3 = np.meshgrid(y, z)
		x31 = np.ones_like(y3)*(ox-l/2)
		x32 = np.ones_like(y3)*(ox+l/2)

		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")
		ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
		ax.set_xbound(0-200, 0+200)
		ax.set_ybound(0-200, 0+200)
		ax.set_zbound(0-200, 0+200)
		# outside surface
		ax.plot_wireframe(x1, y11, z1, color='b', rstride=1, cstride=1, alpha=0.6)
		# inside surface
		ax.plot_wireframe(x1, y12, z1, color='b', rstride=1, cstride=1, alpha=0.6)
		# bottom surface
		ax.plot_wireframe(x2, y2, z21, color='b', rstride=1, cstride=1, alpha=0.6)
		# upper surface
		ax.plot_wireframe(x2, y2, z22, color='b', rstride=1, cstride=1, alpha=0.6)
		# left surface
		ax.plot_wireframe(x31, y3, z3, color='b', rstride=1, cstride=1, alpha=0.6)
		# right surface
		ax.plot_wireframe(x32, y3, z3, color='b', rstride=1, cstride=1, alpha=0.6)
		ax.set_xlabel('X')
		ax.set_xlim(0, 30)
		ax.set_ylabel('Y')
		ax.set_ylim(0, 30)
		ax.set_zlabel('Z')
		ax.set_zlim(0, 30)

		canvas = FigureCanvasTkAgg(fig, master=graphFrame)
		canvas.show()
		canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

		import matplotlib.backends.backend_tkagg as tkagg
		# canvas is your canvas, and root is your parent (Frame, TopLevel, Tk instance etc.)
		tkagg.NavigationToolbar2TkAgg(canvas, graphFrame)
		ax.mouse_init()
		# plt.show()




# comWindow = Tk()
# comMode.com_start(1, '3U', comWindow)


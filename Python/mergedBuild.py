from tkinter import Tk, Button, Label, Frame, StringVar, messagebox, ttk
import time
import serial
import os

ser = 0
BOLD = ('Helvetica', '24', 'bold')
default_cs = '3U'

# --------------------------
class arduino(object):
	# Connect to Arduino
	def serialConnect(controlFrame, connect):
		global ser
		try:
			ser = serial.Serial('COM3', 9600)
			connect.destroy()
			connect = Label(controlFrame, text="Success", font='Calibri 12 bold', fg='green', width=7)
			connect.grid(row=0, column=1)
			if(arduino.waitingOnSerial('STARTUP')):
				ardStatus.set('Arduino Connected')
			ser.close()
			ser.open()

			comStand.config(state='normal')
			moiStand.config(state='normal')

			time.sleep(2)  #at least wait for 2s 
		except serial.SerialException: 
			connect.destroy()
			connect = Label(controlFrame, text="Failed", font='Calibri 12 bold', fg='Red', width=7)
			connect.grid(row=0, column=1)	
			ardStatus.set('Arduino Connection attempt failed, ensure USB port is connected and try again')

	def waitingOnSerial(serialOutput):
		timeout = time.time() + 3	# 3 seconds timeout
		while True:
			bytesToRead=ser.inWaiting()
			if(bytesToRead>0):
				myData = ser.readline()
				myData=str(myData,'utf-8')
				myData = os.linesep.join([s for s in myData.splitlines() if s])
				print('arduinoOutput: '+myData)
				if(myData==serialOutput):
					return True
			if(time.time() > timeout):
				print('TIMEOUT')
				ardStatus.set(ardStatus.get() + '\nTIMEOUT')
				return False
		return False

	def serialPrint(serialInput):
		print('arduinoInput: '+serialInput)
		ser.write(bytes(serialInput, 'UTF-8'))


	def serialRead():
		timeout = time.time() + 3	# 3 seconds timeout
		while True:
			bytesToRead=ser.inWaiting()
			if(bytesToRead>0):
				myData = ser.readline()
				myData=str(myData,'utf-8')
				myData = os.linesep.join([s for s in myData.splitlines() if s])
				return myData
			if(time.time() > timeout):
				print('TIMEOUT')
				ardStatus.set(ardStatus.get() + '\nTIMEOUT')
				return False


# ---------------------------


class mergedBuild(object):
	def  __init__(self):
		from tkinter import ttk
		global cs_config, ardStatus, allButtons
		# Create main application window.
		root = Tk()
		root.title('CubeSat Testing Device')

		# Frame Containers
		titleFrame = Frame(root)
		titleFrame.grid(row=0)
		mainUIFrame = Frame(root, borderwidth=3, relief='groove')
		mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		tabFrame = Frame(root)
		tabFrame.grid(row=2)

		# SubFrame Containers
		controlFrame = Frame(mainUIFrame, borderwidth=3, relief='groove')
		controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		instructionFrame = Frame(mainUIFrame, borderwidth=3, relief='groove')
		instructionFrame.grid(row=0, column=1, sticky='nsew', padx=(10, 10))
		stsFrame = Frame(mainUIFrame, borderwidth=3, relief='groove')
		stsFrame.grid(row=0, column=2, sticky='nsew', padx=10)

		# Title
		titleLabel = Label(titleFrame, text="CubeSat Testing Device", font=BOLD)
		titleLabel.grid(row=0)

		# Arduino Button
		connect = Label(controlFrame, text="", font='Calibri 12 bold', fg='green',width=7)
		connect.grid(row=0, column=1)
		arduinoButton = ttk.Button(controlFrame, command=lambda: arduino.serialConnect(controlFrame, connect) ,text="Connect to Arduino")
		arduinoButton.grid(row=0, column=0, padx=5, sticky='nsew')


		# CubeSat Config selection
		cs_text = Label(controlFrame, text='CubeSat Config:')
		cs_text.grid(row=1, column=0)
		cs_config = StringVar(root)
		cs_config.set(default_cs)
		w = ttk.OptionMenu(controlFrame, cs_config, '', "1U", "2U", "3U")
		w.grid(row = 1, column = 1, sticky='nsew')

		# Calibration Button
		calButton = ttk.Button(controlFrame, command = calMode, text="Calibrate Measurements")
		calButton.grid(row=2, columnspan=2, sticky='nsew')

		# Instructions Label
		ins_text = Label(instructionFrame, text=
		    '1. Place the CubeSat onto the platform with the predefined orientation\n'
		    '2. Ensure the fixturing is properly clamping the CubeSat\n'
		    '3. Select the appropriate config and Mode of operation\n'
		    '4. Calibrate Measurements with the specified block for first time measurements'
		    , justify = 'left', width=60)
		ins_text.grid(row = 0, column = 0, padx=5, sticky='nsew')

		#Status Label
		stslbl = Label(stsFrame, text='Arduino State')
		stslbl.grid(row=0, padx=10, pady=(5,0), sticky='nw')
		ardStatus = StringVar(root)
		ardStatus.set('Arduino not connected')
		status_label = Label(stsFrame, textvariable=ardStatus, justify='left', anchor='nw', font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
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
		comMode.com_start(comFrame)
		moiMode.moi_start(moiFrame)

		# Setup Buttons, disable most for STARTUP MODE
		allButtons = (
			[arduinoButton, 
			comStand, 
			comResetButton, 
			comMeasureButton1, 
			comMeasureButton2, 
			comFinishButton, 
			comTareButton, 
			moiStand, 
			moiResetButton, 
			moiMeasureButton1, 
			moiMeasureButton2, 
			moiMeasureButton3, 
			moiFinishButton])

		buttonInteraction.buttonRefresh([])


		# Allow pressing <Esc> to close the window.
		root.bind('<Escape>', lambda e: root.quit())
		root.protocol("WM_DELETE_WINDOW", lambda: root.quit())	# Quitting Window Exits Program

		# The window is not resizable. 
		root.resizable(0,0) 
		# print ('height:',root.winfo_height())
		# print ('width:',root.winfo_width())

		# Activate the window.
		root.mainloop()

		


"""
==========================================================================================================================================================
CENTER OF MASS MODE
==========================================================================================================================================================
"""

import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot

class comMode():

	def com_start(com_window):
		global com_status_str, com_result_str
		global comStand, comResetButton, comMeasureButton1, comMeasureButton2, comFinishButton, comTareButton
		# Frame Containers
		titleFrame = Frame(com_window)
		titleFrame.grid(row=0, column=0)	
		mainUIFrame = Frame(com_window, borderwidth=3, relief='groove')
		mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		# SubFrame Containers
		controlFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		resultFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		resultFrame.grid(row=0, column=1, sticky='nsew', padx=10)

		# Frames
		instructionFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		instructionFrame.grid(row=0, sticky='nsew', padx=10)
		buttonFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		buttonFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		stsFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		stsFrame.grid(row=2, column=0, sticky='sew', padx=10) 
		graphFrame = Frame(resultFrame, borderwidth=3, relief='groove')
		graphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		printFrame = Frame(resultFrame, borderwidth=3, relief='groove')
		printFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		com_label = Label(titleFrame, text="Centre of Mass Mode", font='Helvetica 16 bold')
		com_label.pack(side='top')


		# Arduino COM Standby button
		comStand = ttk.Button(instructionFrame, text='COM Standby', command=comMode.standby)
		comStand.pack(padx=10, pady=2, fill='both')	

		# Reset Button
		comResetButton = ttk.Button(instructionFrame, text='Reset', command=comMode.reset)
		comResetButton.pack(padx=10, pady=2, fill='both')

		# Tare Button
		comTareButton = ttk.Button(instructionFrame, text='Tare', command=comMode.tare)
		comTareButton.pack(padx=10, pady=2, fill='both')

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
		com_status_str = StringVar(com_window)
		com_status_str.set('Place CubeSat to begin')
		status_label = Label(stsFrame, textvariable=com_status_str, justify='left', anchor='nw', font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=18, width=40, wraplength=320)
		status_label.grid(row=1, padx=10, pady=5)

		comMeasureButton1 = ttk.Button(buttonFrame,text='Orientation 1 Measure', command=comMode.measure1)
		comMeasureButton1.pack(fill='both')
		comMeasureButton2 = ttk.Button(buttonFrame,text='Orientation 2 Measure', command=comMode.measure2)
		comMeasureButton2.pack(fill='both')

		comFinishButton = ttk.Button(buttonFrame,text='Compute Measurements', command=lambda: comMode.finish(graphFrame, resultFrame))
		comFinishButton.pack(fill='both')

		# Plot Center of Mass on 3D axes
		if(cs_config.get()=='3U'):
			comMode.drawGraphs(graphFrame, [15,5,5])
		else:
			comMode.drawGraphs(graphFrame, [5,5,5])


		# Results Textbox
		resultlbl = Label(printFrame, text='Results')
		resultlbl.grid(row=0, padx=10, pady=5, sticky='nw')
		com_result_str = StringVar(com_window)
		com_result_str.set('Results to be printed HERE...')
		result_label = Label(printFrame, textvariable=com_result_str, justify='left', anchor='nw', font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=10, width=80, wraplength=640)
		result_label.grid(row=1, padx=10, pady=5)


	def standby():
		arduino.serialPrint('Q')
		if(arduino.waitingOnSerial('CHGCOM')):
			ardStatus.set('COM Standby Mode')			
			com_status_str.set('Arduino: COM Standby Mode\nAwaiting further instructions')

			buttonInteraction.buttonRefresh([comMeasureButton1, comTareButton, moiStand])

	def reset():
		result = messagebox.askyesno("Reset?", "Are You Sure?\nAll data will be lost", icon='warning')
		if result == True:
			arduino.serialPrint('0')
			if(arduino.waitingOnSerial('RESET')):
				ardStatus.set('COM Standby Mode')
				com_status_str.set('Reset Success\nPlace CubeSat to begin...')

				buttonInteraction.buttonRefresh([comMeasureButton1, comTareButton, moiStand])
		else:
			ardStatus.set('TIMEOUT')


	def tare():
		arduino.serialPrint('T')
		if(arduino.waitingOnSerial('TAREDONE')):
			ardStatus.set('Tare Complete')


	def measure1():
		arduino.serialPrint('W')
		if(arduino.waitingOnSerial('BEGIN_COM1')):
			ardStatus.set('COM Measure 1 State')	
			com_status_str.set('Measuring Orientation 1...')
			
			buttonInteraction.buttonRefresh([comResetButton, comTareButton, comMeasureButton2])
			
			loadCellA = arduino.serialRead()
			loadCellB = arduino.serialRead()
			loadCellC = arduino.serialRead() 

			print(loadCellA)
			print(loadCellB)
			print(loadCellC)

			com_status_str.set('Orientation 1 Measurement Done')
			com_result_str.set(loadCellA+'    '+loadCellB+'    '+loadCellC+'\n')

	def measure2():
		arduino.serialPrint('E')
		if(arduino.waitingOnSerial('BEGIN_COM2')):
			ardStatus.set('COM Measure 2 State')	
			com_status_str.set('Measuring Orientation 2...')
			
			buttonInteraction.buttonRefresh([comResetButton, comTareButton, comFinishButton])

			loadCellA = arduino.serialRead()
			loadCellB = arduino.serialRead()
			loadCellC = arduino.serialRead() 

			print(loadCellA)
			print(loadCellB)
			print(loadCellC)

			com_status_str.set('Orientation 1 Measurement Done')
			com_result_str.set(com_result_str.get()+loadCellA+'    '+loadCellB+'    '+loadCellC+'\n')

	def finish(graphFrame, resultFrame):
		arduino.serialPrint('R')
		if(arduino.waitingOnSerial('COM_DONE')):
			ardStatus.set('COM Standby Mode')			
			com_status_str.set('Computing Results...\n')

			graphFrame.destroy()
			graphFrame = Frame(resultFrame, borderwidth=3, relief='groove')
			graphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
			comMode.drawGraphs(graphFrame, [10,0,0])

			buttonInteraction.buttonRefresh([comResetButton, moiStand])
			
			

	def drawGraphs(graphFrame, com):
		if cs_config.get()=='3U':
			comMode.plot_cuboid(graphFrame, [0, 0, 0], (30, 10, 10), com[0], com[1], com[2])
		elif cs_config.get()=='1U':
			comMode.plot_cuboid(graphFrame, [0, 0, 0], (10, 10, 10), com[0], com[1], com[2])

	def plot_cuboid(graphFrame, center, size, comx,comy,comz):
		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
		from matplotlib.figure import Figure
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt
		import numpy as np
		from itertools import product, combinations

		global canvas, com_point, ax
		ox, oy, oz = center
		l, w, h = size

		x = np.linspace(ox,ox+l,num=10)
		y = np.linspace(oy,oy+w,num=10)
		z = np.linspace(oz,oz+h,num=10)
		x1, z1 = np.meshgrid(x, z)
		y11 = np.ones_like(x1)*(oy)
		y12 = np.ones_like(x1)*(oy+w)
		x2, y2 = np.meshgrid(x, y)
		z21 = np.ones_like(x2)*(oz)
		z22 = np.ones_like(x2)*(oz+h)
		y3, z3 = np.meshgrid(y, z)
		x31 = np.ones_like(y3)*(ox)
		x32 = np.ones_like(y3)*(ox+l)

		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.set_aspect("equal")
		ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
		ax.set_xbound(0-200, 0+200)
		ax.set_ybound(0-200, 0+200)
		ax.set_zbound(0-200, 0+200)
		# outside surface
		ax.plot_wireframe(x1, y11, z1, color='b', rstride=10, cstride=10, alpha=0.6)
		# inside surface
		ax.plot_wireframe(x1, y12, z1, color='b', rstride=10, cstride=10, alpha=0.6)
		# bottom surface
		ax.plot_wireframe(x2, y2, z21, color='b', rstride=10, cstride=10, alpha=0.6)
		# upper surface
		ax.plot_wireframe(x2, y2, z22, color='b', rstride=10, cstride=10, alpha=0.6)
		# left surface
		ax.plot_wireframe(x31, y3, z3, color='b', rstride=10, cstride=10, alpha=0.6)
		# right surface
		ax.plot_wireframe(x32, y3, z3, color='b', rstride=10, cstride=10, alpha=0.6)

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.set_xlim(0, l)
		if(l==30):
			ax.set_ylim(-10, 20)	
			ax.set_zlim(-10, 20)
		else:
			ax.set_ylim(0, 10)	
			ax.set_zlim(0, 10)


	    # draw a point
		com_point = ax.scatter(comx, comy, comz, color="r", s=3)

		canvas = FigureCanvasTkAgg(fig, master=graphFrame)
		canvas.show()
		canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

		# canvas is your canvas, and root is your parent (Frame, TopLevel, Tk instance etc.)
		matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg(canvas, graphFrame)
		ax.mouse_init()


"""
==========================================================================================================================================================
MOMENT OF INERTIA MODE
==========================================================================================================================================================
"""

class moiMode():

	def moi_start(moi_window):
		global moi_status_str, moi_result_str
		global moiStand, moiResetButton, moiMeasureButton1, moiMeasureButton2, moiMeasureButton3, moiFinishButton
		# Frame Containers
		titleFrame = Frame(moi_window)
		titleFrame.grid(row=0, column=0)	
		mainUIFrame = Frame(moi_window, borderwidth=3, relief='groove')
		mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		# SubFrame Containers
		controlFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		resultFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		resultFrame.grid(row=0, column=1, sticky='nsew', padx=10)

		# Frames
		instructionFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		instructionFrame.grid(row=0, sticky='nsew', padx=10)
		buttonFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		buttonFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		stsFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		stsFrame.grid(row=2, column=0, sticky='sew', padx=10) 
		graphFrame = Frame(resultFrame, borderwidth=3, relief='groove')
		graphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		printFrame = Frame(resultFrame, borderwidth=3, relief='groove')
		printFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		moi_label = Label(titleFrame, text="Moment of Inertia Mode", font='Helvetica 16 bold')
		moi_label.pack(side='top')

		# Arduino MOI Standby button
		moiStand = ttk.Button(instructionFrame, text='MOI Standby', command=moiMode.standby)
		moiStand.pack(padx=10, pady=2, fill='both')	

		# Reset Button
		moiResetButton = ttk.Button(instructionFrame, text='Reset', command=moiMode.reset)
		moiResetButton.pack(padx=10, pady=2, fill='both')

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
		moi_status_str = StringVar(moi_window)
		moi_status_str.set('Place CubeSat to begin')
		status_label = Label(stsFrame, textvariable=moi_status_str, justify='left', anchor='nw', font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=16, width=40, wraplength=320)
		status_label.grid(row=1, padx=10, pady=5)	

		# Buttons Layout
		moiMeasureButton1 = ttk.Button(buttonFrame,text='Orientation 1 Measure', command=moiMode.measure1)
		moiMeasureButton1.pack(fill='both')
		moiMeasureButton2 = ttk.Button(buttonFrame,text='Orientation 2 Measure', command=moiMode.measure2)
		moiMeasureButton2.pack(fill='both')
		moiMeasureButton3 = ttk.Button(buttonFrame,text='Orientation 3 Measure', command=moiMode.measure3)
		moiMeasureButton3.pack(fill='both')
		moiFinishButton = ttk.Button(buttonFrame,text='Compute Measurements', command=moiMode.finish)
		moiFinishButton.pack(fill='both')

		# Plot Graph
		moiMode.plot(graphFrame)

		# Results Textbox
		resultlbl = Label(printFrame, text='Results')
		resultlbl.grid(row=0, padx=10, pady=5, sticky='nw')
		moi_result_str = StringVar(moi_window)
		moi_result_str.set('Results to be printed HERE...')
		result_label = Label(printFrame, textvariable=moi_result_str, justify='left', anchor='nw', font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=10, width=80, wraplength=640)
		result_label.grid(row=1, padx=10, pady=5)


	def standby():
		arduino.serialPrint('A')
		if(arduino.waitingOnSerial('CHGMOI')):
			ardStatus.set('MOI Standby Mode')
			moi_status_str.set('Arduino: MOI Standby Mode\nAwaiting further instructions')

			buttonInteraction.buttonRefresh([moiMeasureButton1, comStand])


	def reset():
		result = messagebox.askyesno("Reset?", "Are You Sure?\nAll data will be lost", icon='warning')
		if result == True:
			arduino.serialPrint('0')
			if(arduino.waitingOnSerial('RESET')):
				ardStatus.set('MOI Standby Mode')
				moi_status_str.set('Rotate plate to begin measurement 1')
				moi_status_str.set('Reset Success\nPlace CubeSat to begin...')

				buttonInteraction.buttonRefresh([moiMeasureButton1, comStand])

		else:
			ardStatus.set('TIMEOUT')

		
	def measure1():
		arduino.serialPrint('S')
		if(arduino.waitingOnSerial('BEGIN_MOI1')):
			ardStatus.set('MOI Measure 1 State')
			moi_status_str.set('Rotate plate to begin measurement 1')

			buttonInteraction.buttonRefresh([moiResetButton, moiMeasureButton2])

			oscillations = arduino.serialRead()

			print(oscillations)

			moi_status_str.set('Orientation 1 Measurement Done')
			moi_result_str.set(oscillations)

	def measure2():
		arduino.serialPrint('D')
		if(arduino.waitingOnSerial('BEGIN_MOI2')):
			ardStatus.set('MOI Measure 2 State')
			moi_status_str.set('Rotate plate to begin measurement 2')

			buttonInteraction.buttonRefresh([moiResetButton, moiMeasureButton3])

	def measure3():
		arduino.serialPrint('F')
		if(arduino.waitingOnSerial('BEGIN_MOI3')):
			ardStatus.set('MOI Measure 3 State')
			moi_status_str.set('Rotate plate to begin measurement 3')

			buttonInteraction.buttonRefresh([moiResetButton, moiFinishButton])

	def finish():
		arduino.serialPrint('G')
		if(arduino.waitingOnSerial('MOI_DONE')):
			ardStatus.set('MOI Standby Mode')
			moi_status_str.set('Computing Results...')

			buttonInteraction.buttonRefresh([moiResetButton, comStand])
		

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

"""
==========================================================================================================================================================
Buttons ENABLING AND DISABLING
==========================================================================================================================================================
allButtons [array]
------------
 0: 'connectArduino'
 1: 'comStandby'
 2: 'com_reset'
 3: 'com_m1'
 4: 'com_m2'
 5: 'com_done'
 6: 'tare'
 7: 'moi_standby'
 8: 'moi_reset'
 9: 'moi_m1'
10: 'moi_m2'
11: 'moi_m3'
12: 'moi_done'
"""
class buttonInteraction():
	def buttonRefresh(buttonsToEnable):
		for i in range(1, 13): 
			allButtons[i].config(state='disabled')

		for button in buttonsToEnable:
			button.config(state='normal')

"""
==========================================================================================================================================================
CALIBRATION MODE
==========================================================================================================================================================
"""
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt


class calMode(object):
	def __init__(self):
		global cal_status_str, calType_str, cal_window

		# Setup Window
		cal_window = Tk()
		cal_window.title("CAL Mode")
		# cal_window.geometry('300x200')

		# Frame Containers
		titleFrame = Frame(cal_window)
		titleFrame.grid(row=0, column=0)	
		stsFrame = Frame(cal_window, borderwidth=3, relief='groove')
		stsFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		mainUIFrame = Frame(cal_window, borderwidth=3, relief='groove')
		mainUIFrame.grid(row=2, column=0, sticky='nsew', padx=10)
		comFrame = Frame(cal_window, borderwidth=3, relief='groove')	
		comFrame.grid(row = 3, column = 0, sticky = 'nsew', padx = 10)
		moiFrame = Frame(cal_window, borderwidth=3, relief='groove')
		moiFrame.grid(row = 4, column = 0, sticky = 'nsew', padx = 10)

		# Frames within mainUIFrame Containers
		calOptionFrame = Frame(mainUIFrame)
		calOptionFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		insFrame = Frame(mainUIFrame)
		insFrame.grid(row = 0, column = 1, sticky ='nsew', padx = 10)

		# Frames within comFrame Container
		comFrameUI = Frame(comFrame)
		comFrameUI.grid(row = 0, column = 0, sticky = 'nsew', padx =10)
		graphFrame = Frame(comFrame, borderwidth=3, relief='groove')
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
		cal_status_str = StringVar(cal_window)
		cal_status_str.set('Place Calibration Block to begin')
		status_label = Label(stsFrame, textvariable=cal_status_str, justify='left', anchor='nw', font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=3, width=100, wraplength=640)
		status_label.grid(row=1, column=0, sticky='nw', pady=10, padx=5)

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

"""
==========================================================================================================================================================
==========================================================================================================================================================
"""








# if __name__=='__main__':
mergedBuild()
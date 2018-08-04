from tkinter import Tk, Button, Label, Frame, StringVar, messagebox, ttk, filedialog
import time
import serial
import serial.tools.list_ports
import os
import csv	
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import product, combinations
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
global  count, ser
count = 0



BOLD = ('Helvetica', '24', 'bold')
default_cs = '3U'

# --------------------------
class arduino(object):
	# Connect to Arduino
	def serialConnect(controlFrame, connect):
		global ser
		try:
			# Auto select first serialport (unplug other serialport connections)
			list = serial.tools.list_ports.comports()
			portstr = list[0]
			ser = serial.Serial(str(portstr[0]), 9600)
			connect.destroy()
			connect = Label(controlFrame, text="Success", font='Calibri 12 bold', fg='green', width=7)
			connect.grid(row=0, column=1)
			if(arduino.waitingOnSerial('STARTUP')):
				ardStatus.set('Arduino Connected')
				ser.close()
				ser.open()

				buttonInteraction.buttonRefresh([comStand, moiStand])

				time.sleep(2)  #at least wait for 2s for Arduino to complete  bootup phase
	

		except (serial.SerialException, IndexError) as e: 
			connect.destroy()
			connect = Label(controlFrame, text="Failed", font='Calibri 12 bold', fg='Red', width=7)
			connect.grid(row=0, column=1)	
			ardStatus.set('Arduino Connection attempt failed, ensure USB port is connected and try again')

	# Wait for specific Serial String output (Timeouts after 3 seconds)
	def waitingOnSerial(serialOutput):
		timeout = time.time() + 10	# 3 seconds timeout
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

	# Serial Prints a byte sized character (read as integer in Arduino)
	def serialPrint(serialInput):
		print('arduinoInput: '+serialInput)
		ser.write(bytes(serialInput, 'UTF-8'))

	# Read from the serial port, returns the string
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
				return 'No Data Timeout'

# --------------------------
class osOperations:
	def exportCSV(mode):
		global comData, moiData
		comData = []
		comData.append(['SomeValA','SomeValB','SomeValC'])
		dir_name = filedialog.askdirectory()
		osOperations.writeCSV(dir_name, comData, mode)

	def writeCSV(dir_name, data, mode):	 
		if(mode == 'COM'):
			fileName = '\\COM_Measurements.csv'
		else:
			fileName = '\\MOI_Measurements.csv'	

		with open(dir_name+fileName, 'w', newline='') as csvfile:
		    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

		    if (mode =='COM'):
			    filewriter.writerow(['Orientation 1', '', '', 'Orientation 2', '', '', 'COM Coordinates'])
			    filewriter.writerow(['LoadCellA', 'LoadCellB', 'LoadCellC', 'LoadCellA', 'LoadCellB', 'LoadCellC', 'X', 'Y', 'Z'])
		    elif (mode =='MOI'):
			    filewriter.writerow(['Orientation 1', 'Orientation 2', 'Orientation 3', 'Moment of Inertia'])
			    filewriter.writerow(['Period (s)', 'Period (s)', 'Period (s)', 'X', 'Y', 'Z'])

		    for i in data:
			    filewriter.writerow(i)
		    os.startfile(dir_name)
		



# ---------------------------
"""
Main GUI with COM and MOI modes as subframes
"""
class mergedBuild(object):

	def  __init__(self):
		# from tkinter import ttk
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
		w = ttk.OptionMenu(controlFrame, cs_config, '', "1U", "2U", "3U", "TEST", command=mergedBuild.refreshGraph)
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
		tabsView = ttk.Notebook(tabFrame)
		comFrame = Frame(tabsView)
		moiFrame = Frame(tabsView)
		tabsView.add(comFrame, text='Center of Mass')
		tabsView.add(moiFrame, text='Moment of Inertia')
		tabsView.pack(side='top', fill='both', padx=0, pady=5)


		# Setup COM and MOI Mode
		com = comMode()
		com.com_start(comFrame)
		moi = moiMode()
		moi.moi_start(moiFrame)

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
			moiFinishButton,
			calButton])

		buttonInteraction.buttonRefresh([])


		# Allow pressing <Esc> to close the window.
		root.bind('<Escape>', lambda e: root.quit())
		root.protocol("WM_DELETE_WINDOW", lambda: root.quit())	# Closing Window Exits Program

		# The window is not resizable. 
		root.resizable(0,0) 
		# print ('height:',root.winfo_height())
		# print ('width:',root.winfo_width())
		w = root.winfo_width()
		h = root.winfo_height()

		root.geometry('%dx%d+%d+%d' % (w, h, 50, 50))
		# Activate the window.
		root.mainloop()

	# Refreshes COM Graph plot
	def refreshGraph(myObject):
		global comGraphFrame, comResultFrame, com_status_str
		comGraphFrame.destroy()
		comGraphFrame = Frame(comResultFrame, borderwidth=3, relief='groove')
		comGraphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		comMode.drawGraphs(comGraphFrame,[100,100,100], 'done')

		if(cs_config.get()=='TEST'):
			com_status_str.set('Place Test Block on Plate')
		else:
			com_status_str.set('Place CubeSat to begin')

"""
==========================================================================================================================================================
CENTER OF MASS MODE
==========================================================================================================================================================
"""



class comMode():

	def com_start(self, com_window):
		global com_status_str, com_result_str, comGraphFrame, comResultFrame
		global comStand, comResetButton, comMeasureButton1, comMeasureButton2, comFinishButton, comTareButton
		# Frame Containers
		titleFrame = Frame(com_window)
		titleFrame.grid(row=0, column=0)	
		mainUIFrame = Frame(com_window, borderwidth=3, relief='groove')
		mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		# SubFrame Containers
		controlFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		comResultFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		comResultFrame.grid(row=0, column=1, sticky='nsew', padx=10)

		# Frames
		instructionFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		instructionFrame.grid(row=0, sticky='nsew', padx=10)
		buttonFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		buttonFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		stsFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		stsFrame.grid(row=2, column=0, sticky='sew', padx=10) 
		comGraphFrame = Frame(comResultFrame, borderwidth=3, relief='groove')
		comGraphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		printFrame = Frame(comResultFrame, borderwidth=3, relief='groove')
		printFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		com_label = Label(titleFrame, text="Centre of Mass Mode", font='Helvetica 16 bold')
		com_label.pack(side='top')


		# Arduino COM Standby button
		comStand = ttk.Button(instructionFrame, text='COM Standby', command=comMode.standby)
		comStand.pack(padx=10, pady=1, fill='both')	

		# Reset Button
		comResetButton = ttk.Button(instructionFrame, text='Reset', command=comMode.reset)
		comResetButton.pack(padx=10, pady=1, fill='both')

		# Tare Button
		comTareButton = ttk.Button(instructionFrame, text='Tare', command=comMode.tare)
		comTareButton.pack(padx=10, pady=1, fill='both')

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
		status_label.config(height=15, width=40, wraplength=320)
		status_label.grid(row=1, padx=10, pady=5)
		exportButton = ttk.Button(stsFrame, text='Export to CSV', command=lambda: osOperations.exportCSV('COM'))
		exportButton.grid(row=2, padx=10, pady=5, sticky='nsew')

		comMeasureButton1 = ttk.Button(buttonFrame,text='Orientation 1 Measure (X-axis)', command=comMode.measure1)
		comMeasureButton1.pack(fill='both')
		comMeasureButton2 = ttk.Button(buttonFrame,text='Orientation 2 Measure (Y-axis)', command=comMode.measure2)
		comMeasureButton2.pack(fill='both')

		comFinishButton = ttk.Button(buttonFrame,text='Compute Measurements', command=lambda: comMode.finish(comGraphFrame, comResultFrame))
		comFinishButton.pack(fill='both')

		# Plot 3D axes with invalid COM point
		if(cs_config.get()=='3U'):
			comMode.drawGraphs(comGraphFrame, [100,100,0],'done')
		elif (cs_config.get()=='1U'):
			comMode.drawGraphs(comGraphFrame, [100,100,0],'done')
		elif (cs_config.get()=='TEST'):
			comMode.drawGraphs(comGraphFrame, [100,100,0],'done') 


		# Results Textbox
		resultlbl = Label(printFrame, text='Results')
		resultlbl.grid(row=0, padx=10, pady=5, sticky='nw')
		com_result_str = StringVar(com_window)
		com_result_str.set('Results to be printed HERE...')
		result_label = Label(printFrame, textvariable=com_result_str, justify='left', anchor='nw', font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=8, width=80, wraplength=640)
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
			ardStatus.set(ardStatus.get()+'\n'+'Tare Complete')


	def measure1():
		# YZ coordinates
		global loadCell1A, loadCell1B, loadCell1C, comGraphFrame
		arduino.serialPrint('W')
		if(arduino.waitingOnSerial('BEGIN_COM1')):
			ardStatus.set('COM Measure 1 State')	
			com_status_str.set('Measuring Orientation 1...')
			
			buttonInteraction.buttonRefresh([comResetButton, comTareButton, comMeasureButton2])
			
			# time.sleep(1)
			loadCell1AStr = arduino.serialRead()
			loadCell1A = float(loadCell1AStr.lstrip('A: '))
			loadCell1BStr = arduino.serialRead()
			loadCell1B = float(loadCell1BStr.lstrip('B: '))
			loadCell1CStr = arduino.serialRead() 
			loadCell1C = float(loadCell1CStr.lstrip('C: '))

			if(arduino.waitingOnSerial('END_COM1')):

				print(loadCell1AStr)
				print(loadCell1BStr)
				print(loadCell1CStr)

				loadCell1AStr = 'A: 172.55'
				loadCell1BStr = 'B: 124.12'
				loadCell1CStr = 'C: 201.34'

				com_status_str.set('Orientation 1 Measurement Done')
				com_result_str.set(loadCell1AStr+'    '+loadCell1BStr+'    '+loadCell1CStr+'\n')

				# For TESTING
				if(cs_config.get()=='TEST'):
					# comCoord = comMode.testCOM()
					comCoord = [12.01, 18.11]
					comGraphFrame.destroy()
					comGraphFrame = Frame(comResultFrame, borderwidth=3, relief='groove')
					comGraphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
					comMode.drawGraphs(comGraphFrame, [comCoord[0],comCoord[1],0], 'done')

					com_result_str.set(com_result_str.get()+'X: '+str(comCoord[0])+' ; Y: '+str(comCoord[1])+'\n')


	def testCOM(): # TESTMode COM
		# TEST Preset Values
		D=25
		L=D*0.866 

		# A is placed at (0, 5)
		# B is placed at (8.7, 0)
		# C is placed at (8.7, 10)

		# Only for TESTING purposes
		W = loadCell1A+loadCell1B+loadCell1C

		# Orientation 1 (default frame 0)
		fromA_x1 = (loadCell1B+loadCell1C)*L/W		
		fromA_y1 = (loadCell1C-loadCell1B)*D/(2*W)

		fromO_x1 = fromA_x1
		fromO_y1 = (D/2) + fromA_y1

		print(fromO_x1)
		print(fromO_y1)

		return [fromO_x1, fromO_y1]

	def measure2():
		# XZ coordinates
		global loadCell2A, loadCell2B, loadCell2C, graphFrame
		arduino.serialPrint('E')
		if(arduino.waitingOnSerial('BEGIN_COM2')):
			ardStatus.set('COM Measure 2 State')	
			com_status_str.set('Measuring Orientation 2...')
			
			buttonInteraction.buttonRefresh([comResetButton, comTareButton, comFinishButton])

			loadCell2AStr = arduino.serialRead()
			loadCell2A = float(loadCell2AStr.lstrip('A: '))
			loadCell2BStr = arduino.serialRead()
			loadCell2B = float(loadCell2BStr.lstrip('B: '))
			loadCell2CStr = arduino.serialRead() 
			loadCell2C = float(loadCell2CStr.lstrip('C: '))


			print(loadCell2AStr)
			print(loadCell2BStr)
			print(loadCell2CStr)

			com_status_str.set('Orientation 1 Measurement Done')
			com_result_str.set(com_result_str.get()+loadCell2AStr+'    '+loadCell2BStr+'    '+loadCell2CStr+'\n')

	def finish(graphFrame, resultFrame):
		global comGraphFrame

		arduino.serialPrint('R')
		if(arduino.waitingOnSerial('COM_DONE')):
			ardStatus.set('COM Standby Mode')			
			com_status_str.set('Computing Results...\n')
			
			comCoord = comMode.calcCOM()

			comGraphFrame.destroy()
			comGraphFrame = Frame(comResultFrame, borderwidth=3, relief='groove')
			comGraphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
			comMode.drawGraphs(comGraphFrame, [comCoord[0],comCoord[1],comCoord[2]], 'done')

			com_result_str.set(com_result_str.get()+'X: '+str(comCoord[0])+' ; Y: '+str(comCoord[1])+' ; Z: '+str(comCoord[2])+'\n')

			buttonInteraction.buttonRefresh([comResetButton, moiStand])
			
	def calcCOM():
		# COM Preset Values
		CS_h = 34.5
		CS_w = 10
		D = 20
		L = D*math.sin(math.pi/3) 
		r = (D/2)/math.sin(math.pi/3)
		theta = math.radians(30)

		# In Frame 1 (Triangle Frame)
		# A is placed at (0, 8.08)
		# B is placed at (-7, -4.04)
		# C is placed at (7, -4.04)

		# Only for TESTING purposes
		# loadCell1A = 500
		# loadCell1B = 500
		# loadCell1C = 1500 - loadCell1B - loadCell1A
		# loadCell2A = 500
		# loadCell2B = 500
		# loadCell2C = 1500 - loadCell2A - loadCell2B

		W = loadCell1A+loadCell1B+loadCell1C

		# Orientation 1 (default frame 1)
		fromA_z1 = (loadCell1B+loadCell1C)*L/W		
		fromA_y1 = (loadCell1C-loadCell1B)*D/(2*W)

		p1 = np.matrix([[0],[fromA_y1],[r - fromA_z1]])

		# Rotate to frame 0 (rotate about x)
		O10 = np.matrix([[0],[CS_w/2],[CS_h/2]])
		cos1 = math.cos((math.pi/2)-theta)
		sin1 = math.sin((math.pi/2)-theta)
		R10 = np.matrix([[1,0,0],[0,cos1,-sin1],[0,sin1,cos1]])
		p0_1 = R10*p1 + O10

		# Orientation 2 (Rotate about z axis 90 degrees)
		fromA_x2 = (loadCell2B+loadCell2C)*L/W		
		fromA_z2 = (loadCell2C-loadCell2B)*D/(2*W) 

		p2 = np.matrix([[r - fromA_x2],[0],[fromA_z2]])

		# Rotate to frame 0 (rotate about y)
		O20 = np.matrix([[CS_w/2],[0],[CS_h/2]])
		cos2 = math.cos(-theta)
		sin2 = math.sin(-theta)
		R20 = np.matrix([[cos2,0,sin2],[0,1,0],[-sin2,0,cos2]])
		p0_2 = R20*p2 + O20
		
		# Average to z values 
		p0_z = (float(p0_2[2]) + float(p0_1[2]))/2

		print('O1z: ',float(p0_1[2]))
		print('O2z: ',float(p0_2[2]))

		p0 = np.matrix([[float(p0_2[0])],[float(p0_1[1])],[p0_z]])

		print(p0)

		return [float(p0[0]), float(p0[1]), float(p0[2])]


	def drawGraphs(graphFrame, com, rotation):
		if cs_config.get()=='3U':
			comMode.plot_cuboid(comGraphFrame, [0, 0, 0], (10, 10, 30), com[0], com[1], com[2], rotation)
		elif cs_config.get()=='2U':
			comMode.plot_cuboid(comGraphFrame, [0, 0, 0], (10, 10, 20), com[0], com[1], com[2], rotation)
		elif cs_config.get()=='1U':
			comMode.plot_cuboid(comGraphFrame, [0, 0, 0], (10, 10, 10), com[0], com[1], com[2], rotation)
		elif cs_config.get()=='TEST':
			comMode.plot_cuboid(comGraphFrame, [0, 0, 0], (25, 25, 0), com[0], com[1], com[2], rotation)

	def plot_cuboid(graphFrame, center, size, comx,comy,comz, rotation):

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

		if(h==30):
			ax.set_xlim(-10, 20)
			ax.set_ylim(-10, 20)	
			ax.set_zlim(0, 30)
			segmentLine = 3
		elif(h==20):
			ax.set_xlim(-5, 15)
			ax.set_ylim(-5, 15)	
			ax.set_zlim(0, 20)	
			segmentLine= 5
		elif(h==10):
			ax.set_xlim(0, 10)
			ax.set_ylim(0, 10)	
			ax.set_zlim(0, 10)
			segmentLine=10
		else: # TEST MODE
			ax.set_xlim(0, 25)
			ax.set_ylim(0, 25)	
			ax.set_zlim(0, 25)
			segmentLine=10

		# outside surface
		ax.plot_wireframe(x1, y11, z1, color='b', rstride=segmentLine, cstride=10, alpha=0.6)
		# inside surface
		ax.plot_wireframe(x1, y12, z1, color='b', rstride=segmentLine, cstride=10, alpha=0.6)
		# bottom surface
		ax.plot_wireframe(x2, y2, z21, color='b', rstride=10, cstride=10, alpha=0.6)
		# upper surface
		ax.plot_wireframe(x2, y2, z22, color='b', rstride=10, cstride=10, alpha=0.6)
		# left surface
		ax.plot_wireframe(x31, y3, z3, color='b', rstride=segmentLine, cstride=10, alpha=0.6)
		# right surface
		ax.plot_wireframe(x32, y3, z3, color='b', rstride=segmentLine, cstride=10, alpha=0.6)

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		

		if(cs_config.get()=='TEST'):
			distance = 25 				# Straight line distance between adjacent load cells
			length = distance*0.866 	# Length of Normal to the opposite line connecting 2 load cells
			ax.text(0, distance/2, 0, 'A', size=20, zorder=1, color='k')
			ax.text(length, 0, 0, 'B', size=20, zorder=1, color='k')
			ax.text(length, distance, 0, 'C', size=20, zorder=1, color='k')
			# Triangular Line drawing the range of the load cell positions
			AB_x = np.linspace(0,length,50)
			AB_y = np.linspace(distance/2,0,50)
			BC_x = np.linspace(length,length,50)
			BC_y = np.linspace(0,distance,50)
			CA_x = np.linspace(length,0,50)
			CA_y = np.linspace(distance,distance/2,50)
			ax.plot(AB_x, AB_y, 0, label='AB', color='g')
			ax.plot(BC_x, BC_y, 0, label='BC', color='g')
			ax.plot(CA_x, CA_y, 0, label='CA', color='g')

	    # draw a point representing the COM
		if(rotation=='x'):
			#plot line 
			line_x = np.linspace(0,100,50)
			ax.plot(line_x, comy, comz, label='YZ Plot', color='r')

		elif(rotation=='y'):
			line_x = np.linspace(0,100,50)
			line_y = np.linspace(0,100,50)
			ax.plot(line_x, comy, comz, label='YZ Plot', color='r')
			ax.plot(comx, line_y, comz, label='XZ Plot', color='r')
			
		elif(rotation=='done'):	
			com_point = ax.scatter(comx, comy, comz, color="r", s=10)

		canvas = FigureCanvasTkAgg(fig, master=comGraphFrame)
		canvas.show()
		canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

		# canvas is your canvas, and root is your parent (Frame, TopLevel, Tk instance etc.)
		matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg(canvas, comGraphFrame)
		ax.mouse_init()

"""
==========================================================================================================================================================
MOMENT OF INERTIA MODE
==========================================================================================================================================================
"""

class moiMode():

	def moi_start(self, moi_window):
		global moi_status_str, moi_result_str
		global moiStand, moiResetButton, moiMeasureButton1, moiMeasureButton2, moiMeasureButton3, moiFinishButton
		global moiGraphFrame, moiResultFrame
		# Frame Containers
		titleFrame = Frame(moi_window)
		titleFrame.grid(row=0, column=0)	
		mainUIFrame = Frame(moi_window, borderwidth=3, relief='groove')
		mainUIFrame.grid(row=1, column=0, sticky='nsew', padx=10)

		# SubFrame Containers
		controlFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		controlFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		moiResultFrame = Frame(mainUIFrame, borderwidth=0, relief='groove')
		moiResultFrame.grid(row=0, column=1, sticky='nsew', padx=10)

		# Frames
		instructionFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		instructionFrame.grid(row=0, sticky='nsew', padx=10)
		buttonFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		buttonFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		stsFrame = Frame(controlFrame, borderwidth=3, relief='groove')
		stsFrame.grid(row=2, column=0, sticky='sew', padx=10) 
		moiGraphFrame = Frame(moiResultFrame, borderwidth=3, relief='groove')
		moiGraphFrame.grid(row=0, column=0, sticky='nsew', padx=10)
		printFrame = Frame(moiResultFrame, borderwidth=3, relief='groove')
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
			'11. Click finish to obtain final MOI\n',justify='left')
		cs_label.pack(padx=10)

		#Status Label
		stslbl = Label(stsFrame, text='Status Message')
		stslbl.grid(row=0, padx=10, pady=5, sticky='nw')
		moi_status_str = StringVar(moi_window)
		moi_status_str.set('Place CubeSat to begin')
		status_label = Label(stsFrame, textvariable=moi_status_str, justify='left', anchor='nw', font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=14, width=40, wraplength=320)
		status_label.grid(row=1, padx=10, pady=5)
		exportButton = ttk.Button(stsFrame, text='Export to CSV', command=lambda: osOperations.exportCSV('MOI'))
		exportButton.grid(row=2, padx=10, pady=5, sticky='nsew')
	

		# Buttons Layout
		moiMeasureButton1 = ttk.Button(buttonFrame,text='Orientation 1 Measure (X-axis)', command=self.measure1)
		moiMeasureButton1.pack(fill='both')
		moiMeasureButton2 = ttk.Button(buttonFrame,text='Orientation 2 Measure (Y-axis)', command=self.measure2)
		moiMeasureButton2.pack(fill='both')
		moiMeasureButton3 = ttk.Button(buttonFrame,text='Orientation 3 Measure (Z-axis)', command=self.measure3)
		moiMeasureButton3.pack(fill='both')
		moiFinishButton = ttk.Button(buttonFrame,text='Compute Measurements', command=moiMode.finish)
		moiFinishButton.pack(fill='both')

		# Plot Graph
		self.plot(moiGraphFrame, 0)

		# Results Textbox
		resultlbl = Label(printFrame, text='Results')
		resultlbl.grid(row=0, padx=10, pady=5, sticky='nw')
		moi_result_str = StringVar(moi_window)
		moi_result_str.set('Results to be printed HERE...')
		result_label = Label(printFrame, textvariable=moi_result_str, justify='left', anchor='nw', font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=8, width=80, wraplength=640)
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
			count = 0
			if(arduino.waitingOnSerial('RESET')):
				ardStatus.set('MOI Standby Mode')
				moi_status_str.set('Rotate plate to begin measurement 1')
				moi_status_str.set('Reset Success\nPlace CubeSat to begin...')

				buttonInteraction.buttonRefresh([moiMeasureButton1, comStand])

		else:
			ardStatus.set('TIMEOUT')

		
	def measure1(self):
		global moi1_sensor1, moi1_sensor2
		moi1_sensor1 = []
		moi1_sensor2 = []
		arduino.serialPrint('S')
		if(arduino.waitingOnSerial('BEGIN_MOI1')):
			ardStatus.set('MOI Measure 1 State')
			moi_status_str.set('Rotate plate to begin measurement 1')

			buttonInteraction.buttonRefresh([])

			self.plot(moiGraphFrame, 1)
			
			# oscillations = arduino.serialRead()
			oscillations = moiy1
			print(oscillations)

			moi_status_str.set('Orientation 1 Measurement Done')
			moi_result_str.set(oscillations)

	def measure2(self):
		global moi2_sensor1, moi2_sensor2
		moi2_sensor1 = []
		moi2_sensor2 = []
		arduino.serialPrint('D')
		if(arduino.waitingOnSerial('BEGIN_MOI2')):
			ardStatus.set('MOI Measure 2 State')
			moi_status_str.set('Rotate plate to begin measurement 2')
			buttonInteraction.buttonRefresh([])

			self.plot(moiGraphFrame, 2)

	def measure3(self):
		global moi3_sensor1, moi3_sensor2
		moi3_sensor1 = []
		moi3_sensor1 = []
		arduino.serialPrint('F')
		if(arduino.waitingOnSerial('BEGIN_MOI3')):
			ardStatus.set('MOI Measure 3 State')
			moi_status_str.set('Rotate plate to begin measurement 3')
			buttonInteraction.buttonRefresh([])

			self.plot(moiGraphFrame, 3)
	def finish():
		arduino.serialPrint('G')
		if(arduino.waitingOnSerial('MOI_DONE')):
			ardStatus.set('MOI Standby Mode')
			moi_status_str.set('Computing Results...')

			buttonInteraction.buttonRefresh([moiResetButton, comStand])
	
	def updatePlot(self, i, dataPlot):
		global moiGraphShift

		x_window_len = 50

		yi = arduino.serialRead()
		yi = [float(val) for val in yi.split()]
		moiy1.append(yi[0])
		moiy2.append(yi[1])
		x = range(len(moiy1))

		if(len(moiy1) >= x_window_len):
			moiGraphShift+=1
		else:
			moiGraphShift = 0

		moi_ax.clear()
		moi_ax.set_xlim([moiGraphShift, x_window_len+moiGraphShift])
		moi_ax.set_ylim([-5, 1030])
		moi_ax.grid(color = 'gray', linestyle='-', linewidth=0.2)
		moi_ax.plot(x, moiy1, '-b', label='SENSOR1')
		moi_ax.plot(x, moiy2, '-r', label='SENSOR2')
		moi_ax.legend(loc='upper right')

		print (i, ': ', yi)
		if(i==49):
			arduino.serialPrint('0')
			if(dataPlot == 1):
				moi1_sensor1 = moiy1
				moi1_sensor2 = moiy2
				print("moi1_sensor1: ", moi1_sensor1)
				print("moi1_sensor2: ", moi1_sensor2)
				buttonInteraction.buttonRefresh([moiResetButton, moiMeasureButton2])
			elif(dataPlot == 2):
				moi2_sensor1 = moiy1
				moi2_sensor2 = moiy2
				buttonInteraction.buttonRefresh([moiResetButton, moiMeasureButton3])
			elif(dataPlot == 3):
				moi3_sensor1 = moiy1
				moi3_sensor2 = moiy2	
				buttonInteraction.buttonRefresh([moiResetButton, moiFinishButton])

			timeTaken = arduino.serialRead()
			print(timeTaken)			
			self.a.event_source.stop()
			return

	def plot(self, graphFrame, dataPlot):
		global  moiFig, canvas, moiy1, moiy2, moi_ax

		moiy1 = []
		moiy2 = []
		moiFig = plt.figure(figsize=(6.7,5.1))
		moi_ax = moiFig.add_subplot(1,1,1)
		moi_ax.set_xlim([0, 50])
		moi_ax.set_ylim([0, 1023])

		canvas = FigureCanvasTkAgg(moiFig, master=moiGraphFrame)
		canvas.get_tk_widget().grid(row =0,column = 0)
		# matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg(canvas, moiGraphFrame)


		
		if(dataPlot!=0):
			self.a = animation.FuncAnimation(moiFig, self.updatePlot, fargs=(dataPlot,), repeat=False, interval = 1, blit=False)
		

		moiFig.canvas.draw()
		return



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
13: 'calButton'
"""
class buttonInteraction():
	def buttonRefresh(buttonsToEnable):
		for i in range(1, 13): 
			if allButtons[i] not in buttonsToEnable:
				allButtons[i].config(state='disabled')

		for button in buttonsToEnable:
			button.config(state='normal')

"""
==========================================================================================================================================================
CALIBRATION MODE
==========================================================================================================================================================
"""

class calMode(object):
	def __init__(self):
		global cal_status_str, cal_window

		allButtons[13].config(state='disabled') # Disallow  multiple instances of calMode

		# Setup Window
		cal_window = Tk()
		cal_window.title("CAL Mode")
		# cal_window.geometry('300x200')

		# Frame Containers
		titleFrame = Frame(cal_window)
		titleFrame.grid(row=0, column=0)	
		stsFrame = Frame(cal_window, borderwidth=3, relief='groove')
		stsFrame.grid(row=1, column=0, sticky='nsew', padx=10)
		comFrame = Frame(cal_window, borderwidth=3, relief='groove')	
		comFrame.grid(row = 2, column = 0, sticky = 'nsew', padx = 10)
		moiFrame = Frame(cal_window, borderwidth=3, relief='groove')
		moiFrame.grid(row = 3, column = 0, sticky = 'nsew', padx = 10)

		# Frames within comFrame Container
		beginCOMCalFrame = Frame(comFrame, borderwidth=5)
		beginCOMCalFrame.grid(row = 1, column = 0, sticky = 'nsew', padx =2)
		weightCOMCalFrame = Frame(comFrame, borderwidth=3, relief='groove')
		weightCOMCalFrame.grid(row = 1, column = 1, sticky = 'nsew', padx=2)
		
		zeroCOMCalFrame = Frame(comFrame, borderwidth=3, relief='groove')
		zeroCOMCalFrame.grid(row = 1, column = 2, sticky = 'nsew', padx=2)

		readCOMCalFrame = Frame(comFrame, borderwidth=3, relief='groove')
		readCOMCalFrame.grid(row = 1, column = 3, sticky = 'nsew', padx=2)
		scaleCOMCalFrame = Frame(comFrame, borderwidth=3, relief='groove')
		scaleCOMCalFrame.grid(row = 1, column = 4, sticky = 'nsew', padx=2)

		# Frames within moiFrame Container
		controlMOICalFrame = Frame(moiFrame, borderwidth=3, relief='groove')
		controlMOICalFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=2)
		resultsMOICalFrame = Frame(moiFrame, borderwidth=3, relief='groove')
		resultsMOICalFrame.grid(row = 1, column = 1, sticky = 'nsew', padx=2)
		
		# layout all of the main containers
		cal_window.grid_rowconfigure(1, weight=1)
		cal_window.grid_columnconfigure(0, weight=1)

		# Title Label
		cal_label = Label(titleFrame, text="Calibration Mode", font='Helvetica 16 bold')
		cal_label.grid(row=0, column=0)

		# Status Window
		sts_label = Label(stsFrame, text='Status Message: ', justify='left')
		sts_label.pack(anchor='w')
		cal_status_str = StringVar(cal_window)
		cal_status_str.set('Place Calibration Block to begin')
		status_label = Label(stsFrame, textvariable=cal_status_str, justify='left', anchor='nw', font='Arial 10 italic', fg='gray', bd=2, relief='sunken')
		status_label.config(height=3)
		status_label.pack(fill='both')

		# COM Section
		self.comFrameLayout(comFrame, beginCOMCalFrame, weightCOMCalFrame, zeroCOMCalFrame, readCOMCalFrame, scaleCOMCalFrame)

		# MOI Section
		self.moiFrameLayout(moiFrame, controlMOICalFrame, resultsMOICalFrame)



		saveButton = ttk.Button(cal_window, text='Save and Quit', command=self.save)
		saveButton.grid(row=5, column=0, sticky='nse', padx=10, pady=10)

		# The window is not resizable. 
		cal_window.resizable(0,0) 
		cal_window.protocol("WM_DELETE_WINDOW", lambda: self.save())	# Closing Window closes TK


		cal_window.bind('<Escape>', lambda e: self.save())
		# Activate the window.
		cal_window.mainloop()


	def comFrameLayout(self, comFrame, beginCOMCalFrame, weightCOMCalFrame,zeroCOMCalFrame, readCOMCalFrame, scaleCOMCalFrame):
		# COM Section
		global weightA_CAL, weightB_CAL, weightC_CAL, zeroA, zeroB, zeroC, readA, readB, readC, scaleA, scaleB, scaleC

		comlbl = Label(comFrame, text='Center of Mass', font='Helvetica 12 bold')
		comlbl.grid(row=0, column=0)

		calComStandByButton = ttk.Button(beginCOMCalFrame, text = 'StandBy')
		calComStandByButton.pack(fill='both')
		calComBeginButton = ttk.Button(beginCOMCalFrame, text = 'Begin Calibration')
		calComBeginButton.pack(fill='both')
		resetComButton = ttk.Button(beginCOMCalFrame, text = 'Reset')
		resetComButton.pack(fill='both')

		comWeightLbl = Label(weightCOMCalFrame, text = 'Weight (g)')
		comWeightLbl.grid(row=0, column=0, columnspan=2)

		# weightALbl = Label(weightCOMCalFrame, text = 'A: ')
		# weightALbl.grid(row=1, column = 0)
		# weightBLbl = Label(weightCOMCalFrame, text = 'B: ')
		# weightBLbl.grid(row=2, column = 0)	
		# weightCLbl = Label(weightCOMCalFrame, text = 'C: ')
		# weightCLbl.grid(row=3, column = 0)
		weightA_CAL = StringVar(cal_window)
		weightA_CAL.set('weight')
		weightAText = ttk.Entry(weightCOMCalFrame, textvariable = weightA_CAL)
		weightAText.grid(row=1, column=1)
		# weightB_CAL = StringVar(cal_window)
		# weightB_CAL.set('weightB')
		# weightBText = ttk.Entry(weightCOMCalFrame, textvariable = weightB_CAL)
		# weightBText.grid(row=2, column=1)
		# weightC_CAL = StringVar(cal_window)
		# weightC_CAL.set('weightC')
		# weightCText = ttk.Entry(weightCOMCalFrame, textvariable = weightC_CAL)
		# weightCText.grid(row=3, column=1)


		readZeroLbl = Label(zeroCOMCalFrame, text = 'Read Tare Value (RAW)')
		readZeroLbl.grid(row=0, column=0, columnspan=2)
		zeroALbl = Label(zeroCOMCalFrame, text = 'A: ')
		zeroALbl.grid(row=1, column = 0)
		zeroBLbl = Label(zeroCOMCalFrame, text = 'B: ')
		zeroBLbl.grid(row=2, column = 0)	
		zeroCLbl = Label(zeroCOMCalFrame, text = 'C: ')
		zeroCLbl.grid(row=3, column = 0)
		zeroA = StringVar(cal_window)
		zeroA.set('zeroA')
		zeroAText = ttk.Entry(zeroCOMCalFrame, textvariable = zeroA)
		zeroAText.grid(row=1, column=1)
		zeroB = StringVar(cal_window)
		zeroB.set('zeroB')
		zeroBText = ttk.Entry(zeroCOMCalFrame, textvariable = zeroB)
		zeroBText.grid(row=2, column=1)
		zeroC = StringVar(cal_window)
		zeroC.set('zeroC')
		zeroCText = ttk.Entry(zeroCOMCalFrame, textvariable = zeroC)
		zeroCText.grid(row=3, column=1)

		readFinalLbl = Label(readCOMCalFrame, text = 'Read Final Value (RAW)')
		readFinalLbl.grid(row=0, column=0, columnspan=2)
		readALbl = Label(readCOMCalFrame, text = 'A: ')
		readALbl.grid(row=1, column = 0)
		readBLbl = Label(readCOMCalFrame, text = 'B: ')
		readBLbl.grid(row=2, column = 0)	
		readCLbl = Label(readCOMCalFrame, text = 'C: ')
		readCLbl.grid(row=3, column = 0)
		readA = StringVar(cal_window)
		readA.set('readA')
		readAText = ttk.Entry(readCOMCalFrame, textvariable = readA)
		readAText.grid(row=1, column=1)
		readB = StringVar(cal_window)
		readB.set('readB')
		readBText = ttk.Entry(readCOMCalFrame, textvariable = readB)
		readBText.grid(row=2, column=1)
		readC = StringVar(cal_window)
		readC.set('readC')
		readCText = ttk.Entry(readCOMCalFrame, textvariable = readC)
		readCText.grid(row=3, column=1)

		scaleLbl = Label(scaleCOMCalFrame, text = 'Scale Factor (Manual)')
		scaleLbl.grid(row=0, column=0, columnspan=2)
		scaleALbl = Label(scaleCOMCalFrame, text = 'A: ')
		scaleALbl.grid(row=1, column = 0)
		scaleBLbl = Label(scaleCOMCalFrame, text = 'B: ')
		scaleBLbl.grid(row=2, column = 0)	
		scaleCLbl = Label(scaleCOMCalFrame, text = 'C: ')
		scaleCLbl.grid(row=3, column = 0)
		scaleA = StringVar(cal_window)
		scaleA.set('scaleA')
		scaleAText = ttk.Entry(scaleCOMCalFrame, textvariable = scaleA)
		scaleAText.grid(row=1, column=1)
		scaleB = StringVar(cal_window)
		scaleB.set('scaleB')
		scaleBText = ttk.Entry(scaleCOMCalFrame, textvariable = scaleB)
		scaleBText.grid(row=2, column=1)
		scaleC = StringVar(cal_window)
		scaleC.set('scaleC')
		scaleCText = ttk.Entry(scaleCOMCalFrame, textvariable = scaleC)
		scaleCText.grid(row=3, column=1)

		finishCOMCalButton = ttk.Button(comFrame, text = 'Calibrate Load Cells')
		finishCOMCalButton.grid(row=1,column=5, sticky='nsew')



	def moiFrameLayout(self, moiFrame, controlMOICalFrame, resultsMOICalFrame):
		# MOI Section
		global Ix, Iy, Iz, moiConstant

		moilbl = Label(moiFrame, text='Moment of Inertia', font = 'Helvetica 12 bold')
		moilbl.grid(row=0, column=0)

		standbyButton = ttk.Button(controlMOICalFrame, text = 'Stand by')
		standbyButton.grid(row=0,column=0, columnspan = 2 , sticky = 'nsew')
		calBlockFrame = Frame(controlMOICalFrame, borderwidth=3, relief='groove')
		calBlockFrame.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew', padx=2)
		emptyPlateFrame = Frame(controlMOICalFrame, borderwidth=3, relief='groove')
		emptyPlateFrame.grid(row = 2, column = 0, columnspan = 2, sticky = 'nsew', padx=2)
		resetButton = ttk.Button(controlMOICalFrame, text = 'Reset')
		resetButton.grid(row=3, column=0, columnspan = 2, sticky='nsew')
		constantLbl = Label(controlMOICalFrame, text = 'Constant: ')
		constantLbl.grid(row = 4, column = 0, sticky = 'nsew')
		moiConstant = StringVar(cal_window)
		moiConstant.set('4329')
		constantEntry = ttk.Entry(controlMOICalFrame, width = 10, textvariable = moiConstant)
		constantEntry.grid(row = 4, column = 1, sticky = 'nsew')
		calibrateButton = ttk.Button(controlMOICalFrame, text = '\nCalibrate\n')
		calibrateButton.grid(row = 5, column =0, columnspan = 2, sticky = 'nsew')

		blockLbl = ttk.Label(calBlockFrame, text = 'Loaded Calibration', font = 'Helvetica 9 bold')
		blockLbl.grid(row = 0, column = 0, columnspan = 2, sticky  = 'nsew')
		IxLbl = Label(calBlockFrame, text = 'Ix: ')
		IxLbl.grid(row=1, column = 0)
		IyLbl = Label(calBlockFrame, text = 'Iy: ')
		IyLbl.grid(row=2, column = 0)	
		IzLbl = Label(calBlockFrame, text = 'Iz: ')
		IzLbl.grid(row=3, column = 0)
		Ix = StringVar(cal_window)
		Ix.set('Ix')
		IxText = ttk.Entry(calBlockFrame, textvariable = Ix)
		IxText.grid(row=1, column=1)
		Iy = StringVar(cal_window)
		Iy.set('Iy')
		IyText = ttk.Entry(calBlockFrame, textvariable = Iy)
		IyText.grid(row=2, column=1)
		Iz = StringVar(cal_window)
		Iz.set('Iz')
		IzText = ttk.Entry(calBlockFrame, textvariable = Iz)
		IzText.grid(row=3, column=1)

		block1Button = ttk.Button(calBlockFrame, text = 'Orientation 1 (X-axis upwards)')
		block1Button.grid(row = 4, column = 0, columnspan = 2,  sticky = 'nsew')
		block2Button = ttk.Button(calBlockFrame, text = 'Orientation 2 (Y-axis upwards)')
		block2Button.grid(row = 5, column = 0, columnspan = 2,  sticky = 'nsew')
		block3Button = ttk.Button(calBlockFrame, text = 'Orientation 3 (Z-axis upwards)')
		block3Button.grid(row = 6, column = 0, columnspan = 2,  sticky = 'nsew')


		emptyLbl = ttk.Label(emptyPlateFrame, text = 'Unloaded Calibration', font = 'Helvetica 9 bold')
		emptyLbl.grid(row = 0, column = 0, columnspan = 2, sticky  = 'nsew')
		empty1Button = ttk.Button(emptyPlateFrame, text = 'Outer Fixture (X or Y upwards)')
		empty1Button.grid(row = 1, column = 0, columnspan = 2,  sticky = 'nsew')
		empty2Button = ttk.Button(emptyPlateFrame, text = 'Inner Fixture (Z upwards)')
		empty2Button.grid(row = 2, column = 0, columnspan = 2,  sticky = 'nsew')




		# Results Frame
		graphMOICalFrame = Frame(resultsMOICalFrame, borderwidth=3, relief='groove', height = 250)
		graphMOICalFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=2)
		self.plot(resultsMOICalFrame, 0)

		# Results Textbox
		resultlbl = Label(resultsMOICalFrame, text='Results')
		resultlbl.grid(row=1, padx=10, pady=5, sticky='nw')
		calMOIResultsStr = StringVar(cal_window)
		calMOIResultsStr.set('Results to be printed HERE...')
		result_label = Label(resultsMOICalFrame, textvariable=calMOIResultsStr, justify='left', anchor='nw', font='Arial 10', fg='black', bd=2, relief='sunken')
		result_label.config(height=5, width=77, wraplength=616)
		result_label.grid(row=2, padx=10, pady=5)



	def updatePlot(self, i, dataPlot):
		global moiGraphShift

		x_window_len = 50

		yi = arduino.serialRead()
		yi = [float(val) for val in yi.split()]
		moiy1.append(yi[0])
		moiy2.append(yi[1])
		x = range(len(moiy1))

		if(len(moiy1) >= x_window_len):
			moiGraphShift+=1
		else:
			moiGraphShift = 0

		moi_ax.clear()
		moi_ax.set_xlim([moiGraphShift, x_window_len+moiGraphShift])
		moi_ax.set_ylim([-5, 1030])
		moi_ax.grid(color = 'gray', linestyle='-', linewidth=0.2)
		moi_ax.plot(x, moiy1, '-b', label='SENSOR1')
		moi_ax.plot(x, moiy2, '-r', label='SENSOR2')
		moi_ax.legend(loc='upper right')

		print (i, ': ', yi)
		if(i==49):
			arduino.serialPrint('0')
			if(dataPlot == 1):
				moi1_sensor1 = moiy1
				moi1_sensor2 = moiy2
				print("moi1_sensor1: ", moi1_sensor1)
				print("moi1_sensor2: ", moi1_sensor2)
				buttonInteraction.buttonRefresh([moiResetButton, moiMeasureButton2])
			elif(dataPlot == 2):
				moi2_sensor1 = moiy1
				moi2_sensor2 = moiy2
				buttonInteraction.buttonRefresh([moiResetButton, moiMeasureButton3])
			elif(dataPlot == 3):
				moi3_sensor1 = moiy1
				moi3_sensor2 = moiy2	
				buttonInteraction.buttonRefresh([moiResetButton, moiFinishButton])

			timeTaken = arduino.serialRead()
			print(timeTaken)			
			self.a.event_source.stop()
			return

	def plot(self, frame, dataPlot):
		global  moiFig, canvas, moiy1, moiy2, moi_ax

		moiy1 = []
		moiy2 = []
		moiFig = plt.figure(figsize=(6,2.2))
		moi_ax = moiFig.add_subplot(1,1,1)
		moi_ax.set_xlim([0, 50])
		moi_ax.set_ylim([0, 1023])

		canvas = FigureCanvasTkAgg(moiFig, master=frame)
		canvas.get_tk_widget().grid(row =0,column = 0)
		# matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg(canvas, moiGraphFrame)


		
		if(dataPlot!=0):
			self.a = animation.FuncAnimation(moiFig, self.updatePlot, fargs=(dataPlot,), repeat=False, interval = 1, blit=False)
		

		moiFig.canvas.draw()
		return

	def save(self):
		allButtons[13].config(state='enable')
		cal_window.destroy()

"""
==========================================================================================================================================================
==========================================================================================================================================================
"""







# if __name__=='__main__':
mergedBuild()
# calMode()



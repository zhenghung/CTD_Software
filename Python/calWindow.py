import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
from tkinter import *
import serial

global cs_config, ser

def cal_start(ser, cs_config):
	global status_str
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
	status_label.config(height=3, width=50, wraplength=400)
	status_label.grid(row=1, column=0, sticky='nw', pady=10)

	
	



	# Activate the window.
	cal_window.mainloop()

cal_start(0, '3U')
import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
import tkinter
import serial

global cs_config, ser

def cal_start(ser, cs_config):
	cal_window = tkinter.Tk()
	cal_frame = tkinter.Frame(cal_window)
	cal_label = tkinter.Label(cal_window, text="Calibration Mode", font='Helvetica 16 bold')
	cal_label.pack(side='top')

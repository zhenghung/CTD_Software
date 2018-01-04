import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
import tkinter
import serial

global cs_config

def moi_start(cs_config):
	moi_window = tkinter.Tk()
	moi_frame = tkinter.Frame(moi_window)
	moi_label = tkinter.Label(moi_window, text="Moment of Inertia Mode", font='Helvetica 16 bold')
	moi_label.pack(side='top')
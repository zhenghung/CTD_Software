import matplotlib
matplotlib.use('TkAgg')
import numpy
import matplotlib.pyplot
import tkinter
import serial

global cs_config, ser

def com_start(ser, cs_config):
        
        com_window = tkinter.Tk()
        com_frame = tkinter.Frame(com_window)
        com_label = tkinter.Label(com_window, text="Centre of Mass Mode", font='Helvetica 16 bold')
        com_label.pack(side='top')
                        
                        
                        
                        

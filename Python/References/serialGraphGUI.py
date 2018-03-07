#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import *

master = Tk()

f = open('values.txt')

v = StringVar()
w = Label(master, textvariable=v, height=16).pack()

X = [[],[],[],[]]

def update():
    global v, f, X, master

    line = f.readline()
    if line:
        for i, value in enumerate(line.split()):
            X[i].append(value)
        print("Would plot the values now (lists currently containing %d entries)." % len(X[0]))
        v.set(str(X[0][-1]))
        master.after(1, update)
    else:
        master.after(50, update)

master.after(50, update)
master.mainloop()
# """
# ldr.py

# Display analog data from Arduino using Python (matplotlib)

# Author: Mahesh Venkitachalam
# Website: electronut.in
# """

# import sys, serial, argparse
# import numpy as np
# from time import sleep
# from collections import deque

# import matplotlib.pyplot as plt 
# import matplotlib.animation as animation
# global count
# count = 0
    
# # plot class
# class AnalogPlot:
#   # constr
#   def __init__(self, strPort, maxLen):
#       # open serial port
#       self.ser = serial.Serial('COM3', 9600)

#       self.ax = deque([0.0]*maxLen)
#       self.ay = deque([0.0]*maxLen)
#       self.maxLen = maxLen

#   # add to buffer
#   def addToBuf(self, buf, val):
#       if len(buf) < self.maxLen:
#           buf.append(val)
#       else:
#           buf.pop()
#           buf.appendleft(val)

#   # add data
#   def add(self, data):
#       assert(len(data) == 2)
#       self.addToBuf(self.ax, data[0])
#       self.addToBuf(self.ay, data[1])

#   # update plot
#   def update(self, frameNum, a0, a1):
#       global count
#       # count+=1
#       print(count)
#       try:
#           line = self.ser.readline()
#           data = [float(val) for val in line.split()]
#           # print data
#           if(len(data) == 2):
#               self.add(data)
#               a0.set_data(range(self.maxLen), self.ax)
#               a1.set_data(range(self.maxLen), self.ay)
#               count+=1
#       except KeyboardInterrupt:
#           print('exiting')
          
#           return a0, 

#       print("done!")
#       # self.close() 

#   # clean up
#   def close(self):
#       # close serial
#       self.ser.flush()
#       self.ser.close()    

# # main() function
# def main():
#   # create parser
#   # parser = argparse.ArgumentParser(description="LDR serial")
#   # add expected arguments
#   # parser.add_argument('--port', dest='port', required=True)

#   # parse args
#   # args = parser.parse_args()
  
#   #strPort = '/dev/tty.usbserial-A7006Yqh'
#   # strPort = args.
#   strPort = 'COM3'

#   print('reading from serial port %s...' % strPort)

#   # plot parameters
#   analogPlot = AnalogPlot(strPort, 200)

#   print('plotting data...')

#   # set up animation
#   fig = plt.figure()
#   ax = plt.axes(xlim=(0, 200), ylim=(0, 1023))
#   a0, = ax.plot([], [])
#   a1, = ax.plot([], [])
#   count = 0
#   anim = animation.FuncAnimation(fig, analogPlot.update, 
#                                  fargs=(a0, a1),frames=201,repeat=False, 
#                                  interval=50)

#   # show plot
#   plt.show()
  
#   # clean up
#   # analogPlot.close()


#   print('exiting.')
  

# # call main
# if __name__ == '__main__':
#   main()





# #---------Imports
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import tkinter as Tk
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# #---------End of imports

# fig = plt.Figure()

# x = np.arange(0, 2*np.pi, 0.01)        # x-array

# def animate(i):
#     line.set_ydata(np.sin(x+i/10.0))  # update the data
#     return line,

# root = Tk.Tk()

# label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().grid(column=0,row=1)

# ax = fig.add_subplot(111)
# line, = ax.plot(x, np.sin(x))
# ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)

# Tk.mainloop()
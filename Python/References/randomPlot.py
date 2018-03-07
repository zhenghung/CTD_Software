import matplotlib.pyplot as plt
import matplotlib.animation as anim
import serial, os, time
global ser

def serialRead():
        timeout = time.time() + 3   # 3 seconds timeout
        while True:
            bytesToRead=ser.inWaiting()
            if(bytesToRead>0):
                myData = ser.readline()
                myData=str(myData,'utf-8')
                myData = os.linesep.join([s for s in myData.splitlines() if s])
                data = [float(val) for val in myData.split()]
                print(data)
                return data

def plot_cont(fun, xmax):
    global incre
    incre = 0
    y = []
    y2 = []
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlim([0, 50])
    ax.set_ylim([0, 1023])

    def update(i):
        global incre

        yi = serialRead()

        y.append(yi[0])
        y2.append(yi[1])
        x = range(len(y))
        if(len(y) >= 50):
            incre+=1
        else:
            incre = 0

        ax.clear()
        ax.set_xlim([incre, 50+incre])
        ax.set_ylim([0, 1023])
        ax.plot(x, y)
        ax.plot(x, y2)
        print (i, ': ', yi)

    a = anim.FuncAnimation(fig, update, repeat=False, interval = 5)
    plt.show()


ser = serial.Serial('COM3', 9600)
plot_cont(serialRead(),  50)
"""
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import *

class mclass:
    def __init__(self,  window):
        self.window = window
        self.leftframe= Frame (self.window)
        self.rightframe= Frame (self.window)
        self.leftframe.pack (side= LEFT, anchor=N)
        self.rightframe.pack (side=RIGHT, anchor=N)

        self.box = Entry(self.leftframe)
        self.button = Button (self.leftframe, text="check", command=self.plot)
        self.plotlabel= Label (self.leftframe, text="The following is the plot")
        self.box.grid (row=1, column=1)
        self.button.grid(row=2, column= 1)
        self.plotlabel.grid (row=3, column=1)

    def plot (self):
        x=np.array ([0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([0,16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

        fig = plt.Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.scatter(v,x,color='red')
        a.plot(p, range(2 +max(x)),color='blue')
        a.invert_yaxis()

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.rightframe)
        canvas.get_tk_widget().grid(row=1, column= 2)
        canvas.draw()
        def callback(event):
            #print(event.xdata, event.ydata)
            if event.inaxes == a:
                print(event.xdata, event.ydata)
            else:
                print("Ikke i bilde")
            #window.mainloop()
        cid= fig.canvas.mpl_connect('button_press_event', callback )

window= Tk()
start= mclass (window)
window.mainloop()
"""
import numpy as np
a = np.zeros(6)
for i in range(6):
    a[i] = i

b = np.searchsorted(a, -3)
print(len(a))
print(b)


c = 4

h = 10

print(max(c,h), min(c,h))
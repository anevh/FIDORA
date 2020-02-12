########################## En fil kun for testing av syntax etc ########################

"""
a = "HEI"

print(type(a))

a = "3"

try:
    a = float(a)
    print(a)
    print(type(a))
except:
    print("did not work")

"""
"""
A = [[2, 6], [31, 3], [1,9]]
print(A)
A = sorted(A,key=lambda l:l[0])
print(A)

del A[0]
print(A)
"""
"""
A.append([3,2])
print(A[0][:])

print(A)
if 2 in A[1]:
    print("Ja")
if not [3,4] in A:
    print("Nei")


list1 = [item[0] for item in A]
print(list1)


list2 = [3,6,1,8,3]
print(list2)
list3 = sorted(list2)
print(list2)
print(list3)

"""
"""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [100, 100] },}})

style.theme_use("MyStyle")

a_notebook = ttk.Notebook(root, width=200, height=200)
a_tab = ttk.Frame(a_notebook)
a_notebook.add(a_tab, text = 'This is the first tab')
another_tab = ttk.Frame(a_notebook)
a_notebook.add(another_tab, text = 'This is another tab')
a_notebook.pack(expand=True, fill=tk.BOTH)
root.configure(bg='#D68910')
tk.Button(root, text='Some Text!').pack(fill=tk.X)

root.mainloop()
"""

from tkinter import *
#from tkFileDialog import askopenfilename
from PIL import Image, ImageTk

root = Tk()
#root.overrideredirect(True) 
#setting up a tkinter canvas with scrollbars
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
#xscroll = Scrollbar(frame, orient=HORIZONTAL)
#xscroll.grid(row=1, column=0, sticky=E+W)
#yscroll = Scrollbar(frame)
#yscroll.grid(row=0, column=1, sticky=N+S)
canvas = Canvas(frame, bd=0)#, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
#xscroll.config(command=canvas.xview)
#yscroll.config(command=canvas.yview)
frame.pack(fill=BOTH,expand=1)

#adding the image
#File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
img = Image.open("050_100_200_000_025_002.tif")
scaleh = img.width/408
scalev = img.height/508
print(scaleh, scalev)
img = img.resize((408,508))
img = ImageTk.PhotoImage(image=img)
#img = img.subsample(250)  
w = 10 + img.width()
h = 10 + img.height()
root.geometry("%dx%d+0+0" % (w, h))
canvas.create_image(0,0,image=img,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL), cursor='sb_up_arrow')
x_coor = []
y_coor = []
    #function to be called when mouse is clicked

#sjekk at ikke x1-x2 =0
def line(x1, x2, y1, y2, x):
    return ((y1-y2)/(x1-x2))*(x-x1) + y1


def printcoords(event):
    #outputting x and y coords to console
    x_coor.append(event.x)
    y_coor.append(event.y)
    canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
    if (len(x_coor)==1):
        canvas.config(cursor='sb_down_arrow')
    elif(len(x_coor)==2):
        canvas.config(cursor='sb_right_arrow')
    elif(len(x_coor)==3):
        canvas.config(cursor='sb_left_arrow')
    else:
        root.destroy()
    print (event.x,event.y)
    #mouseclick event
canvas.bind("<Button 1>",printcoords)

root.mainloop()
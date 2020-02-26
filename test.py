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
"""
"""
a = 5
b = 4

if(not (a==2 or b==1)):
    print("Hei")

"""
"""
import cv2
cv2Img = cv2.imread("050_100_200_000_025_002.tif", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
print(cv2Img.shape[2])
f = open('calibration.txt', 'r')
lines = f.readlines()
print(len(lines))
for x in lines:
    words = x.split()
    print(words)

"""
"""
f = open("test_fil.txt", 'a')
f.write("teste her!\n")
f.close()
f = open("test_fil.txt", 'a')
f.write("teste her!\n")
f.close()
f = open("test_fil.txt", 'a')
f.write("teste her!\n")
f.close()
f = open("test_fil.txt", 'w')
f.write("hei\n")
f.write("på deg")
f.close()

"""
"""
import numpy as np
A = np.zeros((4,3))
print(A)

"""

"""
import pymedphys
import pydicom
import matplotlib.pyplot as plt
import numpy as np

gamma_options = {
    'dose_percent_threshold': 3,
    'distance_mm_threshold': 3,
    'lower_percent_dose_cutoff': 20,
    'interp_fraction': 10,  # Should be 10 or more for more accurate results
    'max_gamma': 2,
    'random_subset': None,
    'local_gamma': True,
    'ram_available': 2**29,  # 1/2 GB
    'quiet': True
}

grid = 0.5
scale_factor = 1.035
noise = 0.01

xmin = -28
xmax = 28
ymin = -25
ymax = 25

extent = [xmin-grid/2, xmax+grid/2, ymin-grid/2, ymax+grid/2]

x = np.arange(xmin, xmax + grid, grid)
y = np.arange(ymin, ymax + grid, grid)

coords = (y, x)

xx, yy = np.meshgrid(x, y)
dose_ref = np.exp(-((xx/15)**20 + (yy/15)**20))

plt.figure()
plt.title('Reference dose')

plt.imshow(
    dose_ref, clim=(0, 1.04), extent=extent)
plt.colorbar();


dimensions_of_dose_ref = np.shape(dose_ref)
assert dimensions_of_dose_ref[0] == len(coords[0])
assert dimensions_of_dose_ref[1] == len(coords[1])


dose_eval = dose_ref * scale_factor

plt.figure()
plt.title('Evaluation dose')

plt.imshow(
    dose_eval, clim=(0, 1.04), extent=extent)
plt.colorbar();

dose_diff = dose_eval - dose_ref

plt.figure()
plt.title('Dose Difference')

plt.imshow(
    dose_diff,
    clim=(-0.1, 0.1), extent=extent,
    cmap='seismic'
)
plt.colorbar();

gamma_no_noise = pymedphys.gamma(
    coords, dose_ref,
    coords, dose_eval,
    **gamma_options)

plt.figure()
plt.title('Gamma Distribution')

plt.imshow(
    gamma_no_noise, clim=(0, 2), extent=extent,
    cmap='coolwarm')
plt.colorbar()

plt.show()
valid_gamma_no_noise = gamma_no_noise[~np.isnan(gamma_no_noise)]
no_noise_passing = 100 * np.round(np.sum(valid_gamma_no_noise <= 1) / len(valid_gamma_no_noise), 4)

plt.figure()
plt.title(f'Gamma Histogram | Passing rate = {no_noise_passing}%')
plt.xlabel('Gamma')
plt.ylabel('Number of pixels')

plt.hist(valid_gamma_no_noise, 20);
"""

from tkinter import *
from tkinter import ttk

root = Tk()
root.resizable(0,0)
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)
notebook.pressed_index = None
container = Frame(notebook)
container.pack(fill=BOTH, expand=True)
notebook.add(container, text='Mode A')

canvas = Canvas(container, width=200, height=400)
scroll = Scrollbar(container, command=canvas.yview)
canvas.config(yscrollcommand=scroll.set, scrollregion=(0,0,100,1000))
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)

frame = Frame(canvas, bg='white', width=200, height=1000)
canvas.create_window(100, 500, window=frame)

root.mainloop()
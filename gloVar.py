#import necessary packages
import tkinter as tk
from tkinter import StringVar
import numpy as np


#make GUI-window global
global root
root = tk.Tk()


############################## initialize all global vairables ##########################################
global method
method="1"

global filename 
filename=StringVar(root)
filename.set("Error!")

global dir_name
dir_name=StringVar(root)
dir_name.set("Error!")

global saveTo          
saveTo=StringVar(root)
saveTo.set("Error!")

global pName
pName = StringVar(root)
pName.set("Error!")

global DPI
DPI = tk.StringVar(root)
DPI.set("127")

global comet
comet = tk.StringVar(root)
comet.set("1")

global filetype
filetype = tk.StringVar(root)
filetype.set(".dcm") 

global saveAs
saveAs = tk.StringVar(root)
saveAs.set(".dcm")

global savetofolder

global Name


################################# read and globalize the correction matrices ##################################
global correction127_red
with open('output_red_127.txt', 'r') as f:
    correction127_red = [[float(num) for num in line.split(',')] for line in f]
correction127_red = np.matrix(correction127_red)
global correction127_green
with open('output_green_127.txt', 'r') as f:
    correction127_green = [[float(num) for num in line.split(',')] for line in f]
correction127_green = np.matrix(correction127_green)

global correction127_blue
with open('output_blue_127.txt', 'r') as f:
    correction127_blue = [[float(num) for num in line.split(',')] for line in f]
correction127_blue = np.matrix(correction127_blue)

global correction72_red
with open('output_red_72.txt', 'r') as f:
    correction72_red = [[float(num) for num in line.split(',')] for line in f]
correction72_red = np.matrix(correction72_red)

global correction72_green
with open('output_green_72.txt', 'r') as f:
    correction72_green = [[float(num) for num in line.split(',')] for line in f]
correction72_green = np.matrix(correction72_green)

global correction72_blue
with open('output_blue_72.txt', 'r') as f:
    correction72_blue = [[float(num) for num in line.split(',')] for line in f]
correction72_blue = np.matrix(correction72_blue)


global correctionMatrix127
correctionMatrix127 = np.zeros((1270,1016,3))
correctionMatrix127[:,:,0] = correction127_blue[:,:]
correctionMatrix127[:,:,1] = correction127_green[:,:]
correctionMatrix127[:,:,2] = correction127_red[:,:]

global correctionMatrix72
correctionMatrix72 = np.zeros((720,576,3))
correctionMatrix72[:,:,0] = correction72_blue[:,:]
correctionMatrix72[:,:,1] = correction72_green[:,:]
correctionMatrix72[:,:,2] = correction72_red[:,:]

global correctedImage
correctedImage=None
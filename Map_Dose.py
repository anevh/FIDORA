########################### Map dose ###################
import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
     PhotoImage, BOTH, Canvas, N, S, W, E
import os
from os.path import normpath, basename
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import numpy as np
import SimpleITK as sitk
import pydicom
from PIL import Image, ImageTk

def upload_film_data():
    mark_isocenter_window = tk.Toplevel(Globals.tab3)
    mark_isocenter_window.grab_set()

    canvas = Canvas(mark_isocenter_window, bd=0)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)

    mark_isocenter_window.pack(fill=BOTH,expand=1)

    current_folder = os.getcwd()
    os.chdir(os.path.dirname(sys.argv[0]))
    img = Image.open(Globals.map_dose_film_dataset.get())
    scale_horizontal = img.width/408
    scale_vertical = img.height/508
    img = img.resize((408,508))
    img = ImageTk.PhotoImage(image=img)
    os.chdir(current_folder)

    w = 10 + img.width()
    h = 10 + img.height()
    mark_isocenter_window.geometry("%dx%d+0+0" % (w, h))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL), cursor='sb_up_arrow')
    x_coor = []
    y_coor = []

    def findCoords(event):
        x_coor.append(event.x*scale_vertical)
        y_coor.append(event.y*scale_horizontal)
        canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        if (len(x_coor)==1):
            canvas.config(cursor='sb_down_arrow')
        elif(len(x_coor)==2):
            canvas.config(cursor='sb_right_arrow')
        elif(len(x_coor)==3):
            canvas.config(cursor='sb_left_arrow')
        else:
            mark_isocenter_window.destroy()
    

    canvas.bind("<Button 1>",findCoords)

def UploadAction(type, event=None):
    if(type == "FILM"):
        Globals.map_dose_film_dataset.set(filedialog.askopenfilename())
        ext = os.path.splitext(Globals.map_dose_film_dataset.get())[-1].lower()
        if(ext==".tif"):
            upload_film_data()
            return
        elif(ext==""):
            Globals.map_dose_film_dataset.set("Error!") 
        else:
            messagebox.showerror("Error", "The file must be a .tif file")
            Globals.map_dose_film_dataset.set("Error!") 


#laste opp bilde og markere i bildene, egen funksjon
#gammatest, lese opp på det og implementere
#Eksportere figurer og dataset ut av programmet
#må lagre siste kalibrering (spørre hvilken kalibrering bruker vil bruke)
# hvordan er doseplanene lagret.


# Laste opp doseplan (for nå er det en enkel matrise, selvkonstruert.)
# laste opp skannet film, korriger automatisk.
# brukeren spesifiserse posisjon på film
# gjøre film om til dose map (bruke dose response)
# tegne dose plan og dose map fra film
# regne gamma
# tegne gamma pass/fail og variasjoner
# skriv ut all info vi får fra gammatest

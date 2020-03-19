import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
    PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE
import os
from os.path import normpath, basename
from PIL import Image, ImageTk
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import pydicom
import numpy as np
from matplotlib.figure import Figure
import matplotlib as mpl
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def UploadAction(isFilm):
    if(isFilm):
        file = filedialog.askopenfilename()
        ext = os.path.splitext(file)[-1].lower()
        if(ext==".tif"):
            current_folder = os.getcwd()
            parent = os.path.dirname(file)
            os.chdir(parent)
            cv2Img = cv2.imread(basename(normpath(file)), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
            os.chdir(current_folder)            
            cv2Img = cv2.medianBlur(cv2Img, 5)
            Globals.profiles_film_dataset = cv2Img[:,:,2]
            img = Image.open(file)
            if(not (img.width == 1016 or img.width == 576)):
                messagebox.showerror("Error", "Dpi in image has to be 127 or 72")
                return

            canvas_film = Canvas(Globals.profile_film_visual, bd=0)
            canvas_film.grid(row=0, column=0, sticky=N+S+E+W, pady=(5,0))
            Globals.profile_film_visual.grid_columnconfigure(0, weight=0)
            Globals.profile_film_visual.grid_rowconfigure(0, weight=0)
            scale_horizontal = 8
            scale_vertical = 10
            img_scaled = img.resize((scale_horizontal*15, scale_vertical*15), Image.ANTIALIAS)
        
            img_scaled = ImageTk.PhotoImage(image=img_scaled)
        

            canvas_film.create_image(0,0,image=img_scaled,anchor="nw")
            canvas_film.image = img_scaled
            canvas_film.config(scrollregion=canvas_film.bbox(ALL), width=120, height=150)

        elif(ext==""):
            return 
        else:
            messagebox.showerror("Error", "The file must be a *.tif file")
    
    else:
        file = filedialog.askopenfilename()
        ext = os.path.splitext(file)[-1].lower()
        if(ext=='.dcm'):
            doseplan_dataset = pydicom.dcmread(file)
            doseplan_dataset_pixelArray = doseplan_dataset.pixel_array

            ############################ Her må vi senere legge inn posisjon på en eller annen måte! #########################
            doseplan = doseplan_dataset_pixelArray[30,:,:]

            Globals.profiles_doseplan_dataset = doseplan
            doseplan=doseplan_dataset.DoseGridScaling*doseplan*100   #converts from pixel to cGy

            canvas_doseplan = Canvas(Globals.profile_film_visual, bd=0)
            canvas_doseplan.grid(row=1, column=0, sticky=N+S+E+W, pady=(5,0))
            Globals.profile_film_visual.grid_columnconfigure(1, weight=0)
            Globals.profile_film_visual.grid_rowconfigure(1, weight=0)
            
            doseplan = 255*doseplan/np.amax(doseplan)
            doseplan = doseplan.astype('uint8')
            img = Image.fromarray(doseplan, mode='P')


            scale_horizontal = 8
            scale_vertical = 10
            img_scaled = img.resize((scale_horizontal*15, scale_vertical*15), Image.ANTIALIAS)
        
            img_scaled = ImageTk.PhotoImage(image=img_scaled)
        

            canvas_doseplan.create_image(0,0,image=img_scaled,anchor="nw")
            canvas_doseplan.image = img_scaled
            canvas_doseplan.config(scrollregion=canvas_doseplan.bbox(ALL), width=120, height=150)

        elif(ext==""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dmc file")
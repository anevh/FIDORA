import numpy as np
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH
from os.path import normpath, basename
import os
import gloVar
from tkinter import messagebox
import matplotlib.pyplot as plt

# Function to perform det correction using correction matrix
def correctionMatrix():
    dataset = cv2.imread(gloVar.filename.get().lstrip(), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if(dataset is None):
        current_folder = os.getcwd()
        script_path = gloVar.filename.get()
        parent = os.path.dirname(script_path)
        os.chdir(parent)
        dataset=cv2.imread(basename(normpath(script_path)), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        os.chdir(current_folder)
    if(dataset is None):
         messagebox.showerror("Error", "Something has happen. Check that the filename does not contain Æ,Ø,Å")
         return
    
    if(dataset.shape[2] == 3):
        if(gloVar.DPI.get()=="127" and dataset.shape[0]==1270 and dataset.shape[1]==1016):
            gloVar.correctedImage = abs(dataset-gloVar.correctionMatrix127)
        elif(gloVar.DPI.get()=="72" and dataset.shape[0]==720 and dataset.shape[1]==576):
            gloVar.correctedImage = abs(dataset - gloVar.correctionMatrix72)
        else:
            messagebox.showerror("Error","The resolution of the image is not consistent with dpi:" + gloVar.DPI.get())

    else:
        messagebox.showerror("Error","The uploaded image need to be in RGB-format")

    
    

    
   




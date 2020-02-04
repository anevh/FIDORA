########################### Map dose ###################
import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, PhotoImage, BOTH
import os
from os.path import normpath, basename
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import numpy as np
import SimpleITK as sitk
import pydicom
from PIL import Image, ImageTk

def pixelValueToDose(pixelValue):
    a=1
    b=1
    c=1 #må finne disse konstantene 
    return b/(pixelValue - a) + c

def mapDose(img_path):
    dataset = pydicom.dcmread(img_path)
    ds=dataset.pixel_array
    rows, cols = np.shape(ds) #må kanskje ve
    #rows= int(dataset.Rows)
    #cols = int(dataset.Columns)
    #ds= np.pixel_array(ds.PixelData)
    dose_value = np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            dose_value[i,j]=pixelValueToDose(ds[i,j])
    return dose_value #er et bilde med dose-nivåer, med samme dimensjoner som PV-bildet

def compare(img_path2):
    film=mapDose(img_path)
    dosePlanSys=pydicom.dcmread(img_path2)
    ds=dosePlanSys.pixel_array
    rows, cols = np.shape(ds)
    compare_gamma=np.zeros((rows,cols))
    tolerance=5 #ingen ide hva som er akseptabelt avvik her?
    
    for i in range(rows):
        for j in range(cols):
            if (abs(film-dosePlanSys)<tolerance):
                compare_gamma[i,j]=2^16-1 #sett til hvit
            else:
                compare_gamma[i,j]=0 #sett til svart
    return compare_gamma

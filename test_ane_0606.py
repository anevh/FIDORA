########################### Map dose ###################
import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
     PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE
import os
from os.path import normpath, basename
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import numpy as np
import SimpleITK as sitk
import pydicom
from PIL import Image, ImageTk
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def pixel_to_dose(P,a,b,c):
    return c + b/(P-a)

cv2Img = cv2.imread("filmK_001.tif", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
cv2Img = abs(cv2Img-Globals.correctionMatrix127)
cv2Img = np.clip(cv2Img, 0, 65535)
#### LEgg til medianfilter
def calculate_dose_map(cv2Img):
    wid = Globals.map_dose_ROI_x_end.get() - Globals.map_dose_ROI_x_start.get()
    heig = Globals.map_dose_ROI_y_end.get() - Globals.map_dose_ROI_y_start.get()
    print(wid, heig)
    doseMap_film = np.zeros((heig, wid))
    for i in range(heig):
        for j in range(wid):
            doseMap_film[i,j] = pixel_to_dose(cv2Img[Globals.map_dose_ROI_y_start.get()+i,Globals.map_dose_ROI_x_start.get()+j,2], \
                Globals.popt_red[0], Globals.popt_red[1], Globals.popt_red[2])
    

    
    #fig = Figure(figsize=(0.8,0.8))
    #a = fig.add_subplot(111)
    #plot_image = a.pcolormesh(doseMap_film, cmap='viridis', rasterized=True, vmin=0, vmax=600)
    #fig.colorbar(plot_image, ax=a)
    plt.figure()
    plt.imshow(doseMap_film)
    plt.colorbar()
    plt.show()
    #canvas_dosemap_film = FigureCanvasTkAgg(fig,master = Globals.tab3)
    #canvas_dosemap_film.get_tk_widget().place(relwidth=0.3, relheight=0.55, relx = 0.03, rely=0.1)
    #canvas_dosemap_film.draw()
    #plotte dosekartet (dette må være krympet (408,508))
calculate_dose_map(cv2Img)
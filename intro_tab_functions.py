import Globals
import tkinter as tk
import tkinter.ttk 
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, \
    PhotoImage, BOTH, Toplevel, GROOVE, ACTIVE, FLAT, N, S, W, E, ALL, ttk, LEFT, RIGHT, Y,\
    Label, X, END, Button, StringVar, PhotoImage 

#import sympy as sp
#from io import BytesIO

import cv2
import numpy as np
import os
from os.path import normpath, basename
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#matplotlib.rcParams['text.usetex'] = True #lagt til for å kunne skrive latex i string
from scipy.optimize import curve_fit
from scipy.optimize import curve_fit, OptimizeWarning
from PIL import Image, ImageTk
import sys
from datetime import datetime
import re
import warnings
warnings.filterwarnings("error")

def readMore():
    return
    
def createCalibrationWindow():
    new_window = tk.Toplevel(Globals.tab2)
    new_window.geometry("500x500")  #("360x500")
    new_window.grab_set()
    
    new_window_frame = tk.Frame(new_window)
    new_window_frame.config(relief=FLAT, bg='#ffffff', highlightthickness=0)

    new_window_scroll_canvas = tk.Canvas(new_window_frame)
    new_window_scroll_canvas.config(bg='#ffffff', height=450, width=200)
    new_window_scroll_canvas.grid_propagate(0)

    new_window_scroll = ttk.Scrollbar(new_window_frame, command=new_window_scroll_canvas.yview)

    scrollable_frame= tk.Frame(new_window_scroll_canvas)

    scrollable_frame.bind("<Configure>", lambda e: new_window_scroll_canvas.configure(scrollregion=new_window_scroll_canvas.bbox('all')))
    new_window_scroll_canvas.create_window((0,0), window=scrollable_frame, anchor='nw')
    new_window_scroll_canvas.configure(yscrollcommand=new_window_scroll.set)

    new_window_canvas = tk.Canvas(scrollable_frame)
    new_window_canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    new_window_canvas.pack(fill=BOTH, expand=True)

    new_window_frame.pack(expand=True, fill = BOTH)
    new_window_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    new_window_scroll.pack(side=RIGHT, fill=Y)

    #make frame for text box 1
    frame1 = tk.Frame(new_window_canvas, height=400, width=600)
    frame1.grid(row=0, column=0, pady=(10,10), padx=(10,10))
    frame1.config(bd=0, bg='#E5f9ff')

    #insert text
    t1 =tk.Text(frame1)
    t1.grid(in_=frame1,row=0,column=0)
    t1.config(bg='#E5f9ff',fg='#130E07', font=('calibri', '11'))
    txt1="""  
    Calibration...
    """
    t1.insert(END,txt1)
    t1.config(state=DISABLED) #must be done after the text is inserted

    #insert image 1 : orientering
    scan_box_figure = Image.open("orientering.PNG")
    scan_box_figure = scan_box_figure.resize((300, 200), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=0,column=1, columnspan=2,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)
    #####################################################################################33

def createRaystationWindow():
    new_window = tk.Toplevel(Globals.tab2)
    new_window.geometry("500x500")  #("360x500")
    new_window.grab_set()
    
    new_window_frame = tk.Frame(new_window)
    new_window_frame.config(relief=FLAT, bg='#ffffff', highlightthickness=0)

    new_window_scroll_canvas = tk.Canvas(new_window_frame)
    new_window_scroll_canvas.config(bg='#ffffff', height=450, width=200)
    new_window_scroll_canvas.grid_propagate(0)

    new_window_scroll = ttk.Scrollbar(new_window_frame, command=new_window_scroll_canvas.yview)

    scrollable_frame= tk.Frame(new_window_scroll_canvas)

    scrollable_frame.bind("<Configure>", lambda e: new_window_scroll_canvas.configure(scrollregion=new_window_scroll_canvas.bbox('all')))
    new_window_scroll_canvas.create_window((0,0), window=scrollable_frame, anchor='nw')
    new_window_scroll_canvas.configure(yscrollcommand=new_window_scroll.set)

    new_window_canvas = tk.Canvas(scrollable_frame)
    new_window_canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    new_window_canvas.pack(fill=BOTH, expand=True)

    new_window_frame.pack(expand=True, fill = BOTH)
    new_window_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    new_window_scroll.pack(side=RIGHT, fill=Y)

    #make frame for text box 1
    frame1 = tk.Frame(new_window_canvas, height=400, width=600)
    frame1.grid(row=0, column=0, pady=(10,10), padx=(10,10))
    frame1.config(bd=0, bg='#E5f9ff')

    #insert text
    t1 =tk.Text(frame1)
    t1.grid(in_=frame1,row=0,column=0)
    t1.config(bg='#E5f9ff',fg='#130E07', font=('calibri', '11'))
    txt1="""  
    Raystation...
    """
    t1.insert(END,txt1)
    t1.config(state=DISABLED) #must be done after the text is inserted

    #insert image 1 : orientering
    scan_box_figure = Image.open("orientering.PNG")
    scan_box_figure = scan_box_figure.resize((300, 200), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=0,column=1, columnspan=2,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)
    #####################################################################################
  
def createScannerSettingsWindow():
    new_window = tk.Toplevel(Globals.tab2)
    new_window.geometry("500x500")  #("360x500")
    new_window.grab_set()
    
    new_window_frame = tk.Frame(new_window)
    new_window_frame.config(relief=FLAT, bg='#ffffff', highlightthickness=0)

    new_window_scroll_canvas = tk.Canvas(new_window_frame)
    new_window_scroll_canvas.config(bg='#ffffff', height=450, width=200)
    new_window_scroll_canvas.grid_propagate(0)

    new_window_scroll = ttk.Scrollbar(new_window_frame, command=new_window_scroll_canvas.yview)

    scrollable_frame= tk.Frame(new_window_scroll_canvas)

    scrollable_frame.bind("<Configure>", lambda e: new_window_scroll_canvas.configure(scrollregion=new_window_scroll_canvas.bbox('all')))
    new_window_scroll_canvas.create_window((0,0), window=scrollable_frame, anchor='nw')
    new_window_scroll_canvas.configure(yscrollcommand=new_window_scroll.set)

    new_window_canvas = tk.Canvas(scrollable_frame)
    new_window_canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    new_window_canvas.pack(fill=BOTH, expand=True)

    new_window_frame.pack(expand=True, fill = BOTH)
    new_window_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    new_window_scroll.pack(side=RIGHT, fill=Y)

    #make frame for text box 1
    frame1 = tk.Frame(new_window_canvas, height=400, width=600)
    frame1.grid(row=0, column=0, pady=(10,10), padx=(10,10))
    frame1.config(bd=0, bg='#E5f9ff')

    #insert text
    t1 =tk.Text(frame1)
    t1.grid(in_=frame1,row=0,column=0)
    t1.config(bg='#E5f9ff',fg='#130E07', font=('calibri', '11'))
    txt1="""  
    In order to use FIDORA and get reliable results, one should make sure that all these 
    steps and settings are followed.  

    Step 1: Before irradiation \n 
    Step 2: Working with the scanner \n 
    Step 3: Scanner settings \n 
    Step 4: Scanning \n

    Step 1: Before irradiation 

    Before irradiation of the GafChromic EBT3 film, remember to indicate which direction 
    is landscape direction on the film. Each film or film fragment must be marked with an 
    orientation. Film should always keep the same orientation (portrait or landscape) on 
    the scanner, and in this program you must use landscape orientation. Use the marks 
    to place films consistently on the scanner. 
    """
    t1.insert(END,txt1)
    t1.config(state=DISABLED) #must be done after the text is inserted

    #insert image 1 : orientering
    scan_box_figure = Image.open("orientering.PNG")
    scan_box_figure = scan_box_figure.resize((300, 200), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=0,column=1, columnspan=2,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)
    #####################################################################################33
    #make frame2
    frame2 = tk.Frame(new_window_canvas, height=400, width=600)
    frame2.grid(row=1, column=0, pady=(10,10), padx=(10,10))
    frame2.config(bd=0, bg='#E5f9ff')
    #insert text 2
    t2 =tk.Text(frame2)
    t2.grid(in_=frame2,row=0,column=0)
    t2.config(bg='#E5f9ff',font=('calibri', '11'))
    txt2="""
    Step 2: Working with the scanner

    After irradiating the GafChromic EBT3 film, it should be scanned at least 12 
    hours later, with an Epson V750 Pro flat-bed scanner. Center the film on the 
    scanner with a frame. The frame should preferably be of GafChromic film as well, 
    to achieve equal light conditions.In addition to the frame, it is important to 
    use a transparent compression (glass) sheet on top of the film to avoid film 
    curling. This is important to achieve equal optical densities throughout the 
    scanner surface. Also, remember to position the glass sheet so that it covers
    the entire calibration area (the innermost area of the scanner surface). 
    Otherwise one can experience artifacts such as banding. If one wants to change 
    the glass sheet being used, it must be verified before use. That is, it must be 
    checked that the glass sheet itself does not introduce great errors in the 
    scanner readout. 

    The scanner surface and the glass sheet must be cleaned before scanning, and 
    this can be done using regular lens wipes. This is to prevent dust or other 
    contamination to introduce errors in the scanned image. 

    The Epson V750 Pro software should be installed, and can be found here: 
    https://www.epson.no/products/scanners/consumer-scanners/epson-perfection-
    v750-pro/Stotte-og-nedlastinger
    """
    t2.insert(END,txt2)
    t2.config(state=DISABLED) #must be done after the text is inserted
    #insert image 2a : epson_v750_pro
    scan_box_figure = Image.open("epson_v750_pro.PNG")
    scan_box_figure = scan_box_figure.resize((300, 300), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=1,column=1, columnspan=1,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)

    #insert image 2b : scanner_img
    scan_box_figure = Image.open("scanner_img.jpg")
    scan_box_figure = scan_box_figure.resize((300, 300), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=1,column=2, columnspan=1,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)

    
    #make frame 3
    frame3 = tk.Frame(new_window_canvas, height=400, width=600)
    frame3.grid(row=2, column=0, pady=(10,10), padx=(10,10))
    frame3.config(bd=0, bg='#E5f9ff')
    #insert text 3
    t3 =tk.Text(frame3)
    t3.grid(in_=frame3,row=0,column=0)
    t3.config(bg='#E5f9ff',font=('calibri', '11'))
    #text 3
    txt3="""
    Step 3: Scanner settings

    After installation, make sure the scanner software settings are correct:
    1. Mode: Professional mode
    2. Image type: 48-bit Color
    3. Resolution: 127 dpi
    4. Document size: W: 119.4 mm, H: 118.1 mm
    5. Target size: Original 
    6. Adjustments: No adjustments should be made, as this might interfere with the
    correction made in this program. 

    Make sure your settings are in accordance with the image to the right. 
    """
    t3.insert(END,txt3)
    t3.config(state=DISABLED) #must be done after the text is inserted
    #insert image 3
    scan_box_figure = Image.open("epsonScan.PNG")
    scan_box_figure = scan_box_figure.resize((240, 400), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=2,column=1, columnspan=2,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)
    ##############################################################################
    #make frame 4
    frame4 = tk.Frame(new_window_canvas, height=400, width=600)
    frame4.grid(row=3, column=0, pady=(10,10), padx=(10,10))
    frame4.config(bd=0, bg='#E5f9ff')
    #insert text 4
    t4 =tk.Text(frame4)
    t4.grid(in_=frame4,row=0,column=0)
    t4.config(bg='#E5f9ff',font=('calibri', '11'))

    txt4="""
    Step 4: Scanning

    When all settings are correct, you are ready to scan. First perform 3-5 warm-up 
    scans, in order to stabilize the light source. This can be done by pressing “Scan” 
    about 4 times, and storing the image files in an appropriate folder. Make sure to 
    store the file as Multi-TIFF (*.tif). When scanning, try to make another scan every 
    minute. At this rate, the scanner light source will keep stable, and neither warm-up 
    nor cool down, and thus create similar lighting conditions at each scan.

    After performing 3-5 warm-up scans you are ready to scan the actual scans that can 
    be used in further analysis. Press “Scan”, and again make sure you store the file 
    as a Multi-TIFF file. Remember, to always scan approximately every minute. If many 
    minutes passes without scanning, one should perform an additional round of 3-5 
    warm-up scans to stabilize the light source once again. 
    """
    t4.insert(END,txt4)
    t4.config(state=DISABLED)
    #insert image 4
    scan_box_figure = Image.open("fileSaveSetting.PNG")
    scan_box_figure = scan_box_figure.resize((400, 400), Image.ANTIALIAS) #(width, height)
    scan_figure = ImageTk.PhotoImage(scan_box_figure)
    scan_figure_label = Label(new_window_canvas, image=scan_figure)
    scan_figure_label.image = scan_figure
    scan_figure_label.grid(row=3,column=1, columnspan=2,sticky=N+S+W+E, pady=(0,10))
    scan_figure_label.config(bg='#FFF')#,height=10, width=10)
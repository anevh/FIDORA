import gloVar
import os
from os.path import normpath, basename
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog
import re
import sys
from CorrectionFunctions import *
from cv2 import CV_16U
import numpy as np
import SimpleITK as sitk
import pydicom
from tkinter import filedialog, PhotoImage




# Get filetype from radiobuttons
#def fileType():
#    t = gloVar.filetype.get()
#    gloVar.saveAs.set(t)
#    return t
    
# Get dpi from radiobuttons
def WhatDPI():
    dpi = gloVar.DPI.get()
    return dpi

# Get correction method from radiobuttons (Only one available per desember 2019)
def WhatMethod():
    gloVar.method = gloVar.comet.get()

# Upload image to be corrected
def UploadAction(event=None):
    gloVar.filename.set(filedialog.askopenfilename())
    ext = os.path.splitext(gloVar.filename.get())[-1].lower()
    if(ext==".tif"):
        gloVar.uploaded_file = tk.Text(gloVar.root, height=1, width=1)
        gloVar.uploaded_file.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
        gloVar.uploaded_file.insert(INSERT, basename(normpath(gloVar.filename.get()))) 
        gloVar.uploaded_file.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FDFEFE')
    elif(ext==""):
        gloVar.filename.set("Error!") 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")
        gloVar.filename.set("Error!") 

    
# Choose folder to save corrected image
def Export_File():
    gloVar.dir_name.set(filedialog.askdirectory())
    os.chdir(gloVar.dir_name.get())
    exp_tex=tk.Text(gloVar.root, height=1, width=1)
    exp_tex.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.57)
    exp_tex.insert(INSERT, basename(normpath(gloVar.dir_name.get())))
    exp_tex.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FDFEFE')

# Reset all widgets in case of a restart
def reSet():
    gloVar.filename.set("Error!")
    uploaded_text = tk.Text(gloVar.root, height=1, width=1)
    uploaded_text.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
    uploaded_text.insert(INSERT," ")
    uploaded_text.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FDFEFE')

    gloVar.dir_name.set("Error!")
    folder_box = tk.Text(gloVar.root, height=1, width=1)
    folder_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.57)
    folder_box.insert(INSERT," ")
    folder_box.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FDFEFE') 

    gloVar.saveTo.set("Error!")
    gloVar.savetofolder= tk.Text(gloVar.root, height=1, width=1)
    gloVar.savetofolder.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.66)
    gloVar.savetofolder.insert(INSERT, " " )
    gloVar.savetofolder.config(state=NORMAL, bd=0, font=('calibri', '12'), bg ='#CCD1D1')

    gloVar.pName.set("Error!")
    gloVar.PatientName= tk.Text(gloVar.root, height=1, width=1)
    gloVar.PatientName.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.74)
    gloVar.PatientName.insert(INSERT, " " )
    gloVar.PatientName.config(state=NORMAL, bd=0, font=('calibri', '12'), bg ='#CCD1D1')
    
    
# Help file
def openHelp():
    window = tk.Toplevel(gloVar.root)
    window.geometry("610x600")
    window.config(bg='#FADBD8')
    window.title('CoMet')
    window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='logo.png'))
    window.iconbitmap(default='logo.png')
    help_text = tk.Text(window, height=1, width=1)
    help_text.place(relwidth=0.943, relheight=1, relx=0.01, rely=0.02)
    help_text.insert(INSERT,"\n \
If you have problems read through this guide on how to use the program:\n \
First, click on upload, and choose the tiff-file (.tif) you want to correct. \n \
It must be a tiff-file. Then choose the desired dpi (spatial resolution), \n \
and the file format you want outputted. The only option id (.dcm).\n\n \
If you choose (.tif), the corrected file will be a black-white TIFF-file. \n \
Otherwise, if you choose (.dcm), the corrected file will be a RGB DICOM-file. \n \
Per today, there is only one correction method implemented, but it is possible \n \
to extend the correction method performed at a later time. \n\n \
Now, click on browse, and choose the destination of where you want to save your \n \
corrected file. Add a filename, and press save filename afterwards. This is \n \
required. Note that the maximum number of characters allowed is 20, and that \n \
the characters can only be numbers or letters. \n \
(No Norwegian special characters allowed.) \n\n \
Add a patient name if desired, and press save name afterwards. \n \
This is not required. If you want to add a patient name, note that the maximum \n \
number of characters allowed is 30, and that no space is allowed. (For instance, \n \
“KariNormann” is allowed, but “Kari Normann” is not allowed.) \n\n \
Lastly, press correct, and you will be informed that your filename is corrected. \n \n \
After correction a new tiff-file will appear where it was saved. Even though the \n \
image looks very similar to before correction, it has been changed. The correction \n \
method performed is subtle, and the corrected file is difficult to tell apart \n \
from the uncorrected file, but the program has altered the image slightly.")
    help_text.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FADBD8')
    

# About file
def openAbout():
    window = tk.Toplevel(gloVar.root)
    window.geometry("610x300")
    window.config(bg='#FADBD8')
    window.title('CoMet')
    window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='logo.png'))
    window.iconbitmap(default='logo.png')
    help_text = tk.Text(window, height=1, width=1)
    help_text.place(relwidth=0.95, relheight=1, relx=0.01, rely=0.02)
    help_text.insert(INSERT,"\n \
This python-based program can be used for correction of scanned film images, \n \
performed by the Epson v750 pro flatbed scanner. The correction is necessary \n \
since the flatbed scanner used (Epson v750 pro) has imperfect readout over the \n \
scanner surface. Therefore, CoMet will produce a correction matrix and subtract \n \
it from the scanned film, outputting the corrected image which can considered \n \
to be free of scanner induced errors. The file of interest must be a tiff-file (.tif)\n \
and can be uploaded and saved in a desired folder after correction if performed. \n\n \
This program was made by physics students Stine Gustavsen and Ane Vigre Håland \n \
during the autumn of 2019 as a part of a project and was ready to use in late December.  \n\n \
Last update was at the 18th of December 2019.  ")
    help_text.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FADBD8')

# Get that user has filled inn everything
def checkAllWidgets(*args):
    if(gloVar.filename.get()=="Error!" or gloVar.dir_name.get()=="Error!" or gloVar.saveTo.get()=="Error!"):
        return False
    else:
        return True

# Run correct-button
def Correct():     
    if(checkAllWidgets() is False):
        messagebox.showerror("Error", "All boxes must be filled")
        return
    current_folder = os.getcwd()
    os.chdir(gloVar.dir_name.get())
    if(os.path.exists(gloVar.dir_name.get() + '/' + gloVar.saveTo.get().lstrip() + gloVar.saveAs.get()) is True):
        answer = simpledialog.askstring("Input", "The file already exists. Write another filename",parent=gloVar.root)
        if(answer is None):
            return
        else:
            gloVar.saveTo.set(answer)
            Correct()
    os.chdir(current_folder)
    
    
    if (gloVar.method == "1"):
        correctionMatrix()
    
    if (gloVar.correctedImage is None):
        conf_tex=tk.Text(gloVar.root, height=1, width=1)
        conf_tex.place(relwidth=0.4, relheight=0.14, relx=.5, rely=0.89)
        conf_tex.insert(INSERT, "Error! Image not corrected")
        conf_tex.config(state=DISABLED, bd=0, font=('calibri', '13'), bg ='#D98880', fg='#FBFCFC')
    else:
        conf_tex=tk.Text(gloVar.root, height=1, width=1)
        conf_tex.place(relwidth=0.4, relheight=0.14, relx=.5, rely=0.89)
        conf_tex.insert(INSERT, "File " + gloVar.saveTo.get() + " is saved in folder " +  basename(normpath(gloVar.dir_name.get())))
        conf_tex.config(state=DISABLED, bd=0, font=('calibri', '13'), bg ='#D98880', fg='#FBFCFC')

    R=gloVar.correctedImage[:,:,2];G=gloVar.correctedImage[:,:,1];B=gloVar.correctedImage[:,:,0]
    if(gloVar.DPI.get()=="127"):
        corrImg_dicom = np.zeros((1270,1016,3))
        corrImg_dicom = corrImg_dicom.astype('uint16')
        corrImg_dicom[:,:,0]=R; corrImg_dicom[:,:,1]=G;corrImg_dicom[:,:,2]=B
    elif(gloVar.DPI.get() =="72"):
        corrImg_dicom = np.zeros((720,576,3))
        corrImg_dicom = corrImg_dicom.astype('uint16')
        corrImg_dicom[:,:,0]=R; corrImg_dicom[:,:,1]=G;corrImg_dicom[:,:,2]=B
    else:
        messagebox.showerror("Error", "Wrong DPI in image. No correction")
        
    corrImg_dicom = np.moveaxis(corrImg_dicom,-2,1)
    corrImg_dicom = np.rollaxis(corrImg_dicom,2,0)
    img_dicom = sitk.GetImageFromArray(corrImg_dicom)
    current_folder = os.getcwd()
    os.chdir(gloVar.dir_name.get())
    sitk.WriteImage(img_dicom, gloVar.saveTo.get().lstrip() + gloVar.saveAs.get())
    os.chdir(current_folder)
    mod_NameAndModality = pydicom.dcmread(gloVar.dir_name.get() + '/' + gloVar.saveTo.get().lstrip() + gloVar.saveAs.get())
    mod_NameAndModality.Modality = "RTDOSE"
    if(gloVar.pName.get() != "Error!"):
        mod_NameAndModality.PatientName = gloVar.pName.get()
    else:
        mod_NameAndModality.PatientName = "First^Last"
        
    mod_NameAndModality.save_as(gloVar.dir_name.get() + '/' + gloVar.saveTo.get().lstrip() + gloVar.saveAs.get())


    

    

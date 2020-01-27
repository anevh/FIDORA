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

## Function to do nothing (temp)
def nothingButton():
    return

## Function to upload file
def UploadAction(event=None):
    Globals.CoMet_uploaded_filename.set(filedialog.askopenfilename())
    ext = os.path.splitext(Globals.CoMet_uploaded_filename.get())[-1].lower()
    if(ext==".tif"):
        uploaded_filename = tk.Text(Globals.tab1, height=1, width=1)
        uploaded_filename.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
        uploaded_filename.insert(INSERT, basename(normpath(Globals.CoMet_uploaded_filename.get()))) 
        uploaded_filename.config(state=DISABLED, bd=0, font=('calibri', '12'))
    elif(ext==""):
        Globals.CoMet_uploaded_filename.set("Error!") 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")
        Globals.CoMet_uploaded_filename.set("Error!") 

## Function to set dpi
def setCoMet_dpi():
    dpi = Globals.CoMet_dpi.get()
    print(dpi)
    return dpi

## Function to set the export folder chosen by the user
def setCoMet_export_folder():
    Globals.CoMet_export_folder.set(filedialog.askdirectory())
    if(Globals.CoMet_export_folder.get() == ""):
        #If this: the dialogbox was closed and no folder selected.
        Globals.CoMet_export_folder = "Error!"
    else:
        os.chdir(Globals.CoMet_export_folder.get())
        save_to_folder=tk.Text(Globals.tab1, height=1, width=1)
        save_to_folder.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.57)
        save_to_folder.insert(INSERT, basename(normpath(Globals.CoMet_export_folder.get())))
        save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '12'))

## Function to check that user has filled inn everything
def checkAllWidgets(*args):
    if(Globals.CoMet_uploaded_filename.get()=="Error!" or Globals.CoMet_export_folder.get()=="Error!" or Globals.CoMet_corrected_image_filename.get()=="Error!"):
        return False
    else:
        return True


## Function to perform det correction using correction matrix
def correctionMatrix():
    dataset = cv2.imread(Globals.CoMet_uploaded_filename.get().lstrip(), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if(dataset is None):
        current_folder = os.getcwd()
        script_path = Globals.CoMet_uploaded_filename.get()
        parent = os.path.dirname(script_path)
        os.chdir(parent)
        dataset=cv2.imread(basename(normpath(script_path)), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        os.chdir(current_folder)
    if(dataset is None):
         messagebox.showerror("Error", "Something has happen. Check that the filename does not contain Æ,Ø,Å")
         return
    
    if(dataset.shape[2] == 3):
        if(Globals.CoMet_dpi.get()=="127" and dataset.shape[0]==1270 and dataset.shape[1]==1016):
            Globals.CoMet_correctedImage = abs(dataset-Globals.correctionMatrix127)
        elif(Globals.CoMet_dpi.get()=="72" and dataset.shape[0]==720 and dataset.shape[1]==576):
            Globals.CoMet_correctedImage = abs(dataset - Globals.correctionMatrix72)
        else:
            messagebox.showerror("Error","The resolution of the image is not consistent with dpi:" + Globals.CoMet_dpi.get())

    else:
        messagebox.showerror("Error","The uploaded image need to be in RGB-format")


## Function to perform the correction on the image
def Correct():     
    if(checkAllWidgets() is False):
        messagebox.showerror("Error", "All boxes must be filled")
        return
    current_folder = os.getcwd()
    os.chdir(Globals.CoMet_export_folder.get())
    if(os.path.exists(Globals.CoMet_export_folder.get() + '/' + Globals.CoMet_corrected_image_filename.get().lstrip() + Globals.CoMet_saveAs.get()) is True):
        answer = simpledialog.askstring("Input", "The file already exists. Write another filename",parent=Globals.tab1)
        if(answer is None):
            return
        else:
            Globals.CoMet_corrected_image_filename.set(answer)
            Correct()
    os.chdir(current_folder)
    
    
    correctionMatrix()
    
    if (Globals.CoMet_correctedImage is None):
        Error_message=tk.Text(Globals.tab1, height=1, width=1)
        Error_message.place(relwidth=0.4, relheight=0.14, relx=.5, rely=0.89)
        Error_message.insert(INSERT, "Error! Image not corrected")
        Error_message.config(state=DISABLED, bd=0, font=('calibri', '13'), bg ='#D98880', fg='#FBFCFC')
    else:
        conf_text=tk.Text(Globals.tab1, height=1, width=1)
        conf_text.place(relwidth=0.4, relheight=0.14, relx=.5, rely=0.89)
        conf_text.insert(INSERT, "File " + Globals.CoMet_corrected_image_filename.get() + " is saved in folder " +  basename(normpath(Globals.CoMet_export_folder.get())))
        conf_text.config(state=DISABLED, bd=0, font=('calibri', '13'), bg ='#D98880', fg='#FBFCFC')

    R=Globals.CoMet_correctedImage[:,:,2];G=Globals.CoMet_correctedImage[:,:,1];B=Globals.CoMet_correctedImage[:,:,0]
    if(Globals.CoMet_dpi.get()=="127"):
        corrImg_dicom = np.zeros((1270,1016,3))
        corrImg_dicom = corrImg_dicom.astype('uint16')
        corrImg_dicom[:,:,0]=R; corrImg_dicom[:,:,1]=G;corrImg_dicom[:,:,2]=B
    elif(Globals.CoMet_dpi.get() =="72"):
        corrImg_dicom = np.zeros((720,576,3))
        corrImg_dicom = corrImg_dicom.astype('uint16')
        corrImg_dicom[:,:,0]=R; corrImg_dicom[:,:,1]=G;corrImg_dicom[:,:,2]=B
    else:
        messagebox.showerror("Error", "Wrong DPI in image. No correction")
        
    corrImg_dicom = np.moveaxis(corrImg_dicom,-2,1)
    corrImg_dicom = np.rollaxis(corrImg_dicom,2,0)
    img_dicom = sitk.GetImageFromArray(corrImg_dicom)
    current_folder = os.getcwd()
    os.chdir(Globals.CoMet_export_folder.get())
    sitk.WriteImage(img_dicom, Globals.CoMet_corrected_image_filename.get().lstrip() + Globals.CoMet_saveAs.get())
    os.chdir(current_folder)
    mod_NameAndModality = pydicom.dcmread(Globals.CoMet_export_folder.get() + '/' + Globals.CoMet_corrected_image_filename.get().lstrip() + Globals.CoMet_saveAs.get())
    mod_NameAndModality.Modality = "RTDOSE"
    if(Globals.CoMet_patientName.get() != "Error!"):
        mod_NameAndModality.PatientName = Globals.CoMet_patientName.get()
    else:
        mod_NameAndModality.PatientName = "First^Last"
        
    mod_NameAndModality.save_as(Globals.CoMet_export_folder.get() + '/' + Globals.CoMet_corrected_image_filename.get().lstrip() + Globals.CoMet_saveAs.get())

    ds = pydicom.dcmread(Globals.CoMet_export_folder.get() + '/' + Globals.CoMet_corrected_image_filename.get().lstrip() + Globals.CoMet_saveAs.get() ) # read dicom image
    img = ds.pixel_array # get image array
    RGB_image = np.zeros((img.shape[1], img.shape[2], 3))
    for i in range(img.shape[0]):
        RGB_image[:,:,2-i] = img[i, :,:]

    img8 = (RGB_image/256).astype('uint8')

    
    image_to_canvas =  ImageTk.PhotoImage(image=Image.fromarray(img8))

    height, width, channels = img8.shape

    canvas = tk.Canvas(Globals.tab1, width=width/2, height=height/2)
    canvas.create_image(0,0,image=image_to_canvas)
    canvas.image = image_to_canvas
    canvas.pack()
    

    #canvas = tk.Canvas(Globals.tab1,width=300,height=300)
    #canvas.pack()
    #canvas.create_image(20,20, anchor="nw", image=image_to_canvas)
    #canvas.pack(fill=BOTH, expand=1)
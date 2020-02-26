import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, PhotoImage, BOTH, \
    E, S, N, W
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
        CoMet_uploaded_file_text = tk.Text(Globals.CoMet_border_1_label,  height=1, width=32)
        CoMet_uploaded_file_text.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
        CoMet_uploaded_file_text.insert(INSERT, basename(normpath(Globals.CoMet_uploaded_filename.get())))
        CoMet_uploaded_file_text.config(state=DISABLED, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')

        if (Globals.CoMet_progressbar_check_file):
            Globals.CoMet_progressbar_counter +=1
            Globals.CoMet_progressbar_check_file = False
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25

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
        current_folder = os.getcwd()
        os.chdir(Globals.CoMet_export_folder.get())
        save_to_folder=tk.Text(Globals.CoMet_border_2_label, height=1, width=32)
        save_to_folder.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
        save_to_folder.insert(INSERT, basename(normpath(Globals.CoMet_export_folder.get())))
        save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')
        os.chdir(current_folder)
        if(Globals.CoMet_progressbar_check_folder):
            Globals.CoMet_progressbar_counter +=1
            Globals.CoMet_progressbar_check_folder = False
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        

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
        if(dataset.shape[0]==1270 and dataset.shape[1]==1016):
            Globals.CoMet_correctedImage = abs(dataset-Globals.correctionMatrix127)
        elif(dataset.shape[0]==720 and dataset.shape[1]==576):
            Globals.CoMet_correctedImage = abs(dataset - Globals.correctionMatrix72)
        else:
            messagebox.showerror("Error","The resolution of the image is not consistent with dpi. Must be either 72 or 127")

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
        messagebox.showerror("Error", "The image could not be corrected. Please check all the specifications and try again.")
        Globals.CoMet_progressbar["value"]=0
    else:
        #conf_text=tk.Text(Globals.tab1_canvas)
        #conf_text.grid(row=4, column=3)
        #conf_text.insert(INSERT, "File " + Globals.CoMet_corrected_image_filename.get() + " is saved\n in folder " +  basename(normpath(Globals.CoMet_export_folder.get())))
        #conf_text.config(state=DISABLED, bd=0, font=('calibri', '13'), bg ='#D98880', fg='#FBFCFC')
        #Globals.tab1_canvas.grid_columnconfigure(10, weight=0)
        #Globals.tab1_canvas.grid_rowconfigure(10, weight=0)
        Globals.CoMet_progressbar_counter +=1
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25

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
        messagebox.showerror("Error", "Wrong DPI in image. No correction.\n Please check all specifications and try again.")
        
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
        RGB_image[:,:,i] = img[i, :,:]

 
    img8 = (RGB_image/256).astype('uint8')
    height, width, channels = img8.shape 
    img8 = Image.fromarray(img8, 'RGB')
    
    img8 = img8.resize((250, 300))   
    
    image_to_canvas =  ImageTk.PhotoImage(image=img8)

    Globals.CoMet_print_corrected_image.create_image(123,148,image=image_to_canvas)
    Globals.CoMet_print_corrected_image.image = image_to_canvas
   
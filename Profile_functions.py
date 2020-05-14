import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
    PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE, ACTIVE, \
    FLAT, END, Scrollbar, HORIZONTAL, VERTICAL, ttk, TOP, RIGHT, LEFT
import os
from os.path import normpath, basename
from PIL import Image, ImageTk
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import pydicom
from matplotlib.figure import Figure
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def clearAll():
    Globals.profiles_film_orientation.set('-')
    Globals.profiles_film_orientation_menu.config(state=ACTIVE, bg = '#ffffff', width=15, relief=FLAT)
    
    Globals.profiles_depth.config(state=NORMAL, fg='black')
    Globals.profiles_depth.delete('1.0', END)
    Globals.profiles_depth.insert(INSERT, " ")

    Globals.profiles_iscoenter_coords = []
    Globals.profiles_film_isocenter = None
    Globals.profiles_mark_isocenter_up_down_line = []
    Globals.profiles_mark_isocenter_right_left_line = []
    Globals.profiles_mark_isocenter_oval = []
    Globals.profiles_mark_ROI_rectangle = []
    Globals.profiles_ROI_coords = []

    #if(Globals.profiles_isocenter_check and Globals.profiles_ROI_check):
    #    Globals.profiles_done_button.config(state=DISABLED)
    Globals.profiles_isocenter_check = False
    Globals.profiles_ROI_check = False
    
    #if(Globals.profiles_film_window_open):
    #    Globals.profiles_film_window.destroy()
    #    Globals.profiles_film_window_open = False

    Globals.profiles_upload_button_film.config(state=ACTIVE)
    Globals.profiles_upload_button_doseplan.config(state=DISABLED)
    Globals.profiles_upload_button_rtplan.config(state=DISABLED)

    Globals.profiles_distance_isocenter_ROI = []

    Globals.profiles_film_dataset = None
    Globals.profiles_film_dataset_red_channel = None
    Globals.profiles_film_dataset_ROI = None
    Globals.profiles_film_dataset_ROI_red_channel = None

    Globals.profiles_film_match_isocenter_dataset = np.zeros((7,7))

    Globals.profiles_dataset_doseplan = None
    Globals.profiles_dataset_rtplan = None
    Globals.profiles_longitudinal_displacement_mm = None
    Globals.profiles_lateral_displacement_mm = None
    Globals.profiles_vertical_displacement_mm = None
    Globals.profiles_isocenter_mm = None
    Globals.profiles_test_if_added_rtplan = False
    Globals.profiles_test_if_added_doseplan = False
    return


def pixel_to_dose(P,a,b,c):
    ret = c + b/(P-a)
    return ret

def processDoseplan():

    ################  RT Plan ######################

    #Find each coordinate in mm to isocenter relative to first element in doseplan
    iso_1 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[0] - Globals.profiles_isocenter_mm[0])
    iso_2 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[1] - Globals.profiles_isocenter_mm[1])
    iso_3 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[2] - Globals.profiles_isocenter_mm[2])
    Globals.profiles_isocenter_mm = [iso_1, iso_2, iso_3]

    #Isocenter in pixel relative to the first element in the doseplan
    isocenter_px = np.zeros(3)
    distance_in_doseplan_ROI_reference_point_px = []
    if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
        isocenter_px[0] = np.round(Globals.profiles_isocenter_mm[0])
        isocenter_px[1] = np.round(Globals.profiles_isocenter_mm[1])
        isocenter_px[2] = np.round(Globals.profiles_isocenter_mm[2])
        lateral_displacement_px = np.round(Globals.profiles_lateral_displacement_mm)
        longitudinal_displacement_px = np.round(Globals.profiles_longitudinal_displacement_mm)
        vertical_displacement_px = np.round(Globals.profiles_vertical_displacement_mm)
        
        #Change distance in film to pixel in doseplan
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[0][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[0][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[1][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[1][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[2][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[2][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[3][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[3][1])])
    
    elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
        isocenter_px[0] = np.round(Globals.profiles_isocenter_mm[0]/2)
        isocenter_px[1] = np.round(Globals.profiles_isocenter_mm[1]/2)
        isocenter_px[2] = np.round(Globals.profiles_isocenter_mm[2]/2)
        lateral_displacement_px = np.round(Globals.profiles_lateral_displacement_mm/2)
        longitudinal_displacement_px = np.round(Globals.profiles_longitudinal_displacement_mm/2)
        vertical_displacement_px = np.round(Globals.profiles_vertical_displacement_mm/2)
        
        #Change distance in film to pixel in doseplan
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[0][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[0][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[1][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[1][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[2][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[2][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[3][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[3][1])/2)])

    else:
        isocenter_px[0] = np.round(Globals.profiles_isocenter_mm[0]/3)
        isocenter_px[1] = np.round(Globals.profiles_isocenter_mm[1]/3)
        isocenter_px[2] = np.round(Globals.profiles_isocenter_mm[2]/3)
        lateral_displacement_px = np.round(Globals.profiles_lateral_displacement_mm/3)
        longitudinal_displacement_px = np.round(Globals.profiles_longitudinal_displacement_mm/3)
        vertical_displacement_px = np.round(Globals.profiles_vertical_displacement_mm/3)
        
        #Change distance in film to pixel in doseplan
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[0][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[0][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[1][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[1][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[2][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[2][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[3][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[3][1])/3)])

    reference_point = np.zeros(3)

    ######################## Doseplan ##################################
    #dataset_swapped is now the dataset entered the same way as expected with film (slice, rows, columns)
    #isocenter_px and reference_point is not turned according to the doseplan and film orientation.
    if(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 1, 0]):
        reference_point[1] = isocenter_px[0] + longitudinal_displacement_px
        reference_point[2] = isocenter_px[1] + vertical_displacement_px
        reference_point[0] = isocenter_px[2] + lateral_displacement_px
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #number of frames -> rows
            #rows -> number of frames
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #column -> number of frames
            #number of frames -> rows
            #rows -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        else:
            messagebox.showerror("Error", "Something has gone wrong here.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 0, 1]):
        reference_point[1] = isocenter_px[0] + vertical_displacement_px
        reference_point[2] = isocenter_px[1] + longitudinal_displacement_px
        reference_point[0] = isocenter_px[2] + lateral_displacement_px
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #columns -> number of frames
            #number of frames -> columns
            #rows -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> number of frames
            #number of frames -> rows
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 1, 0, 0]):
        reference_point[1] = isocenter_px[0] + longitudinal_displacement_px
        reference_point[2] = isocenter_px[1] + lateral_displacement_px
        reference_point[0] = isocenter_px[2] + vertical_displacement_px
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> columns
            #columns -> number of frames
            #number of frames -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_iso = isocenter_px[1]
            isocenter_px[1] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #number -> rows
            #colums -> colums
            #rows -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #column -> rows
            #rows -> column
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_iso = isocenter_px[1]
            isocenter_px[1] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 0, 0, 1]):
        reference_point[1] = isocenter_px[0] + lateral_displacement_px
        reference_point[2] = isocenter_px[1] + longitudinal_displacement_px
        reference_point[0] = isocenter_px[2] + vertical_displacement_px
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> rows
            #columns -> number of frames
            #number of frames ->columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #number of frames -> columns
            #columns -> rows
            #rows -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_iso = isocenter_px[1]
            isocenter_px[1] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 1, 0, 0]):
        reference_point[1] = isocenter_px[0] + vertical_displacement_px
        reference_point[2] = isocenter_px[1] + lateral_displacement_px
        reference_point[0] = isocenter_px[2] + longitudinal_displacement_px
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> columns
            #columns -> rows
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_iso = isocenter_px[1]
            isocenter_px[1] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #rows -> number of frames
            #columns -> rows
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_iso = isocenter_px[1]
            isocenter_px[1] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> columns
            #colums -> number of frames
            #number of frames -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 0, 1, 0]):
        reference_point[1] = isocenter_px[0] + lateral_displacement_px
        reference_point[2] = isocenter_px[1] + vertical_displacement_px
        reference_point[0] = isocenter_px[2] + longitudinal_displacement_px
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> number of frames
            #columns ->rows
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[1]
            isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #rows -> columns
            #columns -> rows
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_iso = isocenter_px[1]
            isocenter_px[1] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> rows
            #columns -> number of frames
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_iso = isocenter_px[0]
            isocenter_px[0] = isocenter_px[2]
            isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    else:
        messagebox.showerror("Error", "Something has gone wrong.")
        clearAll()
        return
    


    ####################### Match film and doseplan ###############################

    #Pick the slice where the reference point is (this is the slice-position of the film)
    dose_slice = dataset_swapped[int(reference_point[0]), :, :]
    
    #calculate the coordinated of the Region of Interest in doseplan (marked on the film) 
    #and checks if it actualy exists in dosematrix
    
    doseplan_ROI_coords = []
    top_left_test_side = False; top_left_test_down = False
    top_right_test_side = False; top_right_test_down = False
    bottom_left_test_side = False; bottom_left_test_down = False
    bottom_right_test_side = False; bottom_right_test_down = False
    top_left_side_corr = 0; top_left_down_corr = 0
    top_right_side_corr = 0; top_right_down_corr = 0
    bottom_left_side_corr = 0; bottom_left_down_corr = 0
    bottom_right_side_corr = 0; bottom_right_down_corr = 0


    top_left_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[0][0]
    top_left_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[0][1]
    if(top_left_to_side < 0):
        top_left_test_side = True
        top_left_side_corr = abs(top_left_to_side)
        top_left_to_side = 0
    if(top_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_left_down < 0):
        top_left_test_down = True
        top_left_down_corr = abs(top_left_down)
        top_left_down = 0
    if(top_left_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    
    top_right_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[1][0]
    top_right_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[1][1]
    if(top_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_right_to_side > dose_slice.shape[1]):
        top_right_test_side = True
        top_right_side_corr = top_right_to_side - dose_slice.shape[1]
        top_right_to_side = dose_slice.shape[1]
    if(top_right_down < 0):
        top_right_test_down = True
        top_right_down_corr = abs(top_right_down)
        top_right_down = 0
    if(top_right_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return

    bottom_left_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[2][0]
    bottom_left_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[2][1]
    if(bottom_left_to_side < 0):
        bottom_left_test_side = True
        bottom_left_side_corr = abs(bottom_left_to_side)
        bottom_left_to_side = 0
    if(bottom_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down > dose_slice.shape[0]):
        bottom_left_down_corr = bottom_left_down - dose_slice.shape[0]
        bottom_left_down = dose_slice.shape[0]
        bottom_left_test_down = True
    
    bottom_right_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[3][0]
    bottom_right_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[3][1]
    if(bottom_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_to_side > dose_slice.shape[1]):
        bottom_right_side_corr = bottom_right_to_side - dose_slice.shape[1]
        bottom_right_to_side = dose_slice.shape[1]
        bottom_right_test_side = True
    if(bottom_right_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_down > dose_slice.shape[0]):
        bottom_right_down_corr = bottom_right_down - dose_slice.shape[0]
        bottom_right_down = dose_slice.shape[0]
        bottom_right_test_down = True
    

    if(top_right_test_side or top_right_test_down or top_left_test_side or top_left_test_down \
        or bottom_right_test_side or bottom_right_test_down or bottom_left_test_side or bottom_left_test_down):
        ROI_info = "Left side: " + str(max(top_left_side_corr, bottom_left_side_corr)) + " pixels.\n"\
            + "Right side: " + str(max(top_right_side_corr, bottom_right_side_corr)) + " pixels.\n "\
            + "Top side: " + str(max(top_left_down_corr, top_right_down_corr)) + " pixels.\n"\
            + "Bottom side: " + str(max(bottom_left_down_corr, bottom_right_down_corr)) + " pixels."  
        messagebox.showinfo("ROI info", "The ROI marked on the film did not fit with the size of the doseplan and had to \
            be cut.\n" + ROI_info )

    doseplan_ROI_coords.append([top_left_to_side, top_left_down])
    doseplan_ROI_coords.append([top_right_to_side, top_right_down])
    doseplan_ROI_coords.append([bottom_left_to_side, bottom_left_down])
    doseplan_ROI_coords.append([bottom_right_to_side, bottom_right_down])

    Globals.profiles_doseplan_dataset_ROI = dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
    
    
    img=Globals.profiles_doseplan_dataset_ROI
    if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
        img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
    elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
        img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
    else:
        img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))
    
    #temp_img = np.zeros((img.shape[0], img.shape[1], 3))
    #temp_img[:,:,0]=img;temp_img[:,:,1]=img;temp_img[:,:,2]=img
    #img = temp_img
    #PIL_img_doseplan_ROI = (img/256).astype('uint8')
    #PIL_img_doseplan_ROI = Image.fromarray(PIL_img_doseplan_ROI)
    #PIL_img_doseplan_ROI= PIL_img_doseplan_ROI.convert("P", palette=Image.ADAPTIVE, colors=255)
    mx=np.max(img)
    max_dose = mx*Globals.profiles_dose_scaling_doseplan
    img = img/mx
    PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img)*255))


    wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
    doseplan_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
    doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
    Globals.profiles_film_panedwindow.add(doseplan_canvas, \
        height=max(heig, Globals.profiles_doseplan_text_image.height()), width=wid + Globals.profiles_doseplan_text_image.width())
    doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
        height=max(heig, Globals.profiles_doseplan_text_image.height()), width=wid + Globals.profiles_doseplan_text_image.width())

    doseplan_write_image = tk.Canvas(doseplan_canvas)
    doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
    doseplan_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

    doseplan_text_image_canvas = tk.Canvas(doseplan_canvas)
    doseplan_text_image_canvas.grid(row=0,column=0,sticky=N+S+W+E)
    doseplan_text_image_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
        width=Globals.profiles_doseplan_text_image.width(), height=Globals.profiles_doseplan_text_image.height())

    scaled_image_visual = PIL_img_doseplan_ROI
    scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
    doseplan_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
    doseplan_write_image.image = scaled_image_visual
    doseplan_text_image_canvas.create_image(0,0,image=Globals.profiles_doseplan_text_image)
    doseplan_text_image_canvas.image=Globals.profiles_doseplan_text_image




def UploadRTplan():
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(not(ext == '.dcm')):
        if(ext == ""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dcm file")
            return
    
    current_folder = os.getcwd()
    parent = os.path.dirname(file)
    os.chdir(parent)
    dataset = pydicom.dcmread(file)
    os.chdir(current_folder)
    Globals.profiles_dataset_rtplan = dataset

    #Isocenter given in mm from origo in patient coordinate system
    try:
        isocenter_mm = dataset.BeamSequence[0].ControlPointSequence[0].IsocenterPosition
        Globals.profiles_isocenter_mm = isocenter_mm
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file.")
        return
    
    try:
        lateral_displacement_mm = dataset.PatientSetupSequence[0].TableTopLateralSetupDisplacement
        Globals.profiles_lateral_displacement_mm = lateral_displacement_mm
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file.")
        return

    try:
        longitudinal_displacement_mm = dataset.PatientSetupSequence[0].TableTopLongitudinalSetupDisplacement
        Globals.profiles_longitudinal_displacement_mm = longitudinal_displacement_mm
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file.")
        return

    try:
        vertical_displacement_mm = dataset.PatientSetupSequence[0].TableTopVerticalSetupDisplacement
        Globals.profiles_vertical_displacement_mm = vertical_displacement_mm
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file.")
        return

    Globals.profiles_test_if_added_rtplan = True
    if(Globals.profiles_test_if_added_doseplan):
        processDoseplan()

    Globals.profiles_upload_button_rtplan.config(state=DISABLED)


def UploadDoseplan():
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(not(ext == '.dcm')):
        if(ext == ""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dcm file")
            return
    
    current_folder = os.getcwd()
    parent = os.path.dirname(file)
    os.chdir(parent)
    dataset = pydicom.dcmread(file)
    os.chdir(current_folder)
    doseplan_dataset = dataset.pixel_array

    Globals.profiles_dataset_doseplan = dataset
    Globals.profiles_dose_scaling_doseplan = dataset.DoseGridScaling
    #Check that the resolution is either 1x1x1, 2x2x2 or 3x3x3
    if(not((dataset.PixelSpacing==[1, 1] and dataset.SliceThickness==1) \
        or (dataset.PixelSpacing==[2, 2] and dataset.SliceThickness==2) \
        or (dataset.PixelSpacing==[3, 3] and dataset.SliceThickness==3))):
            messagebox.showerror("Error", "The resolution in doseplan must be 1x1x1, 2x2x2 or 3x3x3")
            return

    #Check that the datamatrix is in right angles to the coordinate system
    if(not(dataset.ImageOrientationPatient==[1, 0, 0, 0, 1, 0] or \
        dataset.ImageOrientationPatient==[1, 0, 0, 0, 0, 1] or \
        dataset.ImageOrientationPatient==[0, 1, 0, 1, 0, 0] or \
        dataset.ImageOrientationPatient==[0, 1, 0, 0, 0, 1] or \
        dataset.ImageOrientationPatient==[0, 0, 1, 1, 0, 0] or \
        dataset.ImageOrientationPatient==[0, 0, 1, 0, 1, 0])):
        messagebox.showerror("Error", "The Image Orientation (Patient) must be parallel to one of the main axis and perpendicular to the two others.")

   
    Globals.profiles_test_if_added_doseplan = True
    if(Globals.profiles_test_if_added_rtplan):
        processDoseplan()

    Globals.profiles_upload_button_doseplan.config(state=DISABLED)


def UploadFilm():
    #if(Globals.profiles_film_window_open):
    #    Globals.profiles_film_window.destroy()
    #    Globals.profiles_film_window_open = False
    if(Globals.profiles_film_orientation.get() == '-'):
        messagebox.showerror("Missing parameter", "Film orientation missing")
        return
    if(Globals.profiles_depth.get("1.0",'end-1c') == " "):
        messagebox.showerror("Missing parameter", "Film depth missing")
        return
    try:
        Globals.profiles_depth_float = float(Globals.profiles_depth.get("1.0", 'end-1c'))
    except:
        messagebox.showerror("Error", "The depth must be a number")
        return
    Globals.profiles_depth.config(state=DISABLED, fg='gray')
    Globals.profiles_film_orientation_menu.configure(state=DISABLED)
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(ext == '.tif'):
        current_folder = os.getcwd()
        parent = os.path.dirname(file)
        os.chdir(parent)
        img = Image.open(file)
        cv2Img = cv2.imread(basename(normpath(file)), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        cv2Img = cv2.medianBlur(cv2Img, 5)
        if(cv2Img is None):
            messagebox.showerror("Error", "Something has gone wrong. Check that the filename does not contain Æ,Ø,Å")
            return
        if(cv2Img.shape[2] == 3):
            if(cv2Img.shape[0]==1270 and cv2Img.shape[1]==1016):
                cv2Img = abs(cv2Img-Globals.correctionMatrix127)
                cv2Img = np.clip(cv2Img, 0, 65535)
            else:
                messagebox.showerror("Error","The resolution of the image is not consistent with dpi")
                return
        else:
            messagebox.showerror("Error","The uploaded image need to be in RGB-format")
            return

        os.chdir(current_folder)            
        Globals.profiles_film_dataset = cv2Img
        Globals.profiles_film_dataset_red_channel = cv2Img[:,:,2]
        if(not (img.width == 1016)):
            messagebox.showerror("Error", "Dpi in image has to be 127")
            return
        
        
        scale_horizontal = 2
        scale_vertical = 2
        img_scaled = img.resize((508, 635), Image.ANTIALIAS)
        img_scaled = ImageTk.PhotoImage(image=img_scaled)
        h = 635 + 20
        w = 508 + 425
        new_window = tk.Toplevel(Globals.tab4)
        new_window.geometry("%dx%d+0+0" % (w, h))
        new_window.grab_set()

        new_window_over_all_frame = tk.Frame(new_window, bd=0, relief=FLAT)
        new_window_over_all_canvas = Canvas(new_window_over_all_frame)

        new_window_xscrollbar = Scrollbar(new_window_over_all_frame, orient=HORIZONTAL, command=new_window_over_all_canvas.xview)
        new_window_yscrollbar = Scrollbar(new_window_over_all_frame, command=new_window_over_all_canvas.yview)

        new_window_scroll_frame = ttk.Frame(new_window_over_all_canvas)
        new_window_scroll_frame.bind("<Configure>", lambda e: new_window_over_all_canvas.configure(scrollregion=new_window_over_all_canvas.bbox('all')))

        new_window_over_all_canvas.create_window((0,0), window=new_window_scroll_frame, anchor='nw')
        new_window_over_all_canvas.configure(xscrollcommand=new_window_xscrollbar.set, yscrollcommand=new_window_yscrollbar.set)

        new_window_over_all_frame.config(highlightthickness=0, bg='#ffffff')
        new_window_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
        new_window_over_all_frame.pack(expand=True, fill=BOTH)
        new_window_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
        new_window_over_all_frame.grid_columnconfigure(0, weight=1)
        new_window_over_all_frame.grid_rowconfigure(0, weight=1)
        new_window_xscrollbar.grid(row=1, column=0, sticky=E+W)
        new_window_over_all_frame.grid_columnconfigure(1, weight=0)
        new_window_over_all_frame.grid_rowconfigure(1, weight=0)
        new_window_yscrollbar.grid(row=0, column=1, sticky=N+S)
        new_window_over_all_frame.grid_columnconfigure(2, weight=0)
        new_window_over_all_frame.grid_rowconfigure(2, weight=0)

        image_canvas = tk.Canvas(new_window_scroll_frame)
        image_canvas.grid(row=0,column=0, rowspan=10, columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
        new_window_scroll_frame.grid_columnconfigure(0, weight=0)
        new_window_scroll_frame.grid_rowconfigure(0, weight=0)

        image_canvas.create_image(0,0,image=img_scaled,anchor="nw")
        image_canvas.image = img_scaled
        image_canvas.config(bg='#ffffff', relief=FLAT, bd=0, scrollregion=image_canvas.bbox(ALL), \
            height=img_scaled.height(), width=img_scaled.width())
        image_canvas.grid_propagate(0)

        film_window_mark_isocenter_text = tk.Text(new_window_scroll_frame, width=55, height=5)
        film_window_mark_isocenter_text.insert(INSERT, \
"When clicking the button \"Mark isocenter\" a window showing \n\
the image will appear and you are to click on the markers \n\
made on the film upon irradiation to find the isocenter. Start \n\
with the marker showing the direction of the film (see the \n\
specifications in main window). When all four marks are made \n\
you will see the isocenter in the image. If you are not happy \n\
with the placement click the button again and repeat.")
        film_window_mark_isocenter_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_isocenter_text.grid(row=0, column=3, rowspan=3, sticky=N+S+E+W, padx=(10,10), pady=(25,0))
        new_window_scroll_frame.columnconfigure(1, weight=0)
        new_window_scroll_frame.rowconfigure(1, weight=0)

        def markIsocenter(img, new_window):
            if(len(Globals.profiles_mark_isocenter_oval)>0):
                image_canvas.delete(Globals.profiles_mark_isocenter_up_down_line[0])
                image_canvas.delete(Globals.profiles_mark_isocenter_right_left_line[0])
                image_canvas.delete(Globals.profiles_mark_isocenter_oval[0])

                Globals.profiles_mark_isocenter_oval=[]
                Globals.profiles_mark_isocenter_right_left_line=[]
                Globals.profiles_mark_isocenter_up_down_line=[]

            Globals.profiles_iscoenter_coords = []
            img_mark_isocenter = ImageTk.PhotoImage(image=img)
            mark_isocenter_window = tk.Toplevel(new_window)
            mark_isocenter_window.geometry("1035x620+10+10")
            mark_isocenter_window.grab_set()

            mark_isocenter_over_all_frame = tk.Frame(mark_isocenter_window, bd=0, relief=FLAT)
            mark_isocenter_over_all_canvas = Canvas(mark_isocenter_over_all_frame)

            mark_isocenter_xscrollbar = Scrollbar(mark_isocenter_over_all_frame, orient=HORIZONTAL, command=mark_isocenter_over_all_canvas.xview)
            mark_isocenter_yscrollbar = Scrollbar(mark_isocenter_over_all_frame, command=mark_isocenter_over_all_canvas.yview)

            mark_isocenter_scroll_frame = ttk.Frame(mark_isocenter_over_all_canvas)
            mark_isocenter_scroll_frame.bind("<Configure>", lambda e: mark_isocenter_over_all_canvas.configure(scrollregion=mark_isocenter_over_all_canvas.bbox('all')))

            mark_isocenter_over_all_canvas.create_window((0,0), window=mark_isocenter_scroll_frame, anchor='nw')
            mark_isocenter_over_all_canvas.configure(xscrollcommand=mark_isocenter_xscrollbar.set, yscrollcommand=mark_isocenter_yscrollbar.set)

            mark_isocenter_over_all_frame.config(highlightthickness=0, bg='#ffffff')
            mark_isocenter_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
            mark_isocenter_over_all_frame.pack(expand=True, fill=BOTH)
            mark_isocenter_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
            mark_isocenter_over_all_frame.grid_columnconfigure(0, weight=1)
            mark_isocenter_over_all_frame.grid_rowconfigure(0, weight=1)
            mark_isocenter_xscrollbar.grid(row=1, column=0, sticky=E+W)
            mark_isocenter_over_all_frame.grid_columnconfigure(1, weight=0)
            mark_isocenter_over_all_frame.grid_rowconfigure(1, weight=0)
            mark_isocenter_yscrollbar.grid(row=0, column=1, sticky=N+S)
            mark_isocenter_over_all_frame.grid_columnconfigure(2, weight=0)
            mark_isocenter_over_all_frame.grid_rowconfigure(2, weight=0)

            mark_isocenter_image_canvas = tk.Canvas(mark_isocenter_scroll_frame)
            mark_isocenter_image_canvas.grid(row=0,column=0, rowspan=10, columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
            mark_isocenter_scroll_frame.grid_columnconfigure(0, weight=0)
            mark_isocenter_scroll_frame.grid_rowconfigure(0, weight=0)

            mark_isocenter_image_canvas.create_image(0,0,image=img_mark_isocenter,anchor="nw")
            mark_isocenter_image_canvas.image = img_mark_isocenter
            mark_isocenter_image_canvas.config(cursor='top_side', bg='#E5f9ff', relief=FLAT, bd=0, \
                scrollregion=mark_isocenter_image_canvas.bbox(ALL), height=img_mark_isocenter.height(), width=img_mark_isocenter.width())
            mark_isocenter_image_canvas.grid_propagate(0)

            def findCoords(event):
                mark_isocenter_image_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
                if(Globals.profiles_iscoenter_coords==[]):
                    Globals.profiles_iscoenter_coords.append([event.x, event.y])
                    mark_isocenter_image_canvas.config(cursor='right_side')

                elif(len(Globals.profiles_iscoenter_coords)==1):
                    Globals.profiles_iscoenter_coords.append([event.x, event.y])
                    Globals.profiles_film_isocenter = [Globals.profiles_iscoenter_coords[0][0], Globals.profiles_iscoenter_coords[1][1]]
                    #el1=0;el2=0
                    #for i in range(-15,16,5):
                    #    for j in range(-15,16,5):
                    #        Globals.profiles_film_match_isocenter_dataset[el1,el2] = \
                    #            Globals.profiles_film_dataset_red_channel[Globals.profiles_film_isocenter[1]+i, Globals.profiles_film_isocenter[0]+j]
                    #        el2+=1
                    #    el2=0;el1+=1
                    x1,y1 = Globals.profiles_iscoenter_coords[0]
                    x4,y4 = Globals.profiles_iscoenter_coords[1]
                    x2 = x1;y3=y4
                    y2=2*Globals.profiles_film_isocenter[1]-y1
                    x3=2*Globals.profiles_film_isocenter[0]-x4
                    up_down_line = image_canvas.create_line(int(x1/2),int(y1/2),int(x2/2),int(y2/2),fill='purple', smooth=1, width=2)
                    right_left_line = image_canvas.create_line(int(x3/2),int(y3/2),int(x4/2),int(y4/2), fill='purple', smooth=1, width=2)
                    oval = image_canvas.create_oval(int(Globals.profiles_film_isocenter[0]/2)-3, int(Globals.profiles_film_isocenter[1]/2)-3,\
                         int(Globals.profiles_film_isocenter[0]/2)+3, int(Globals.profiles_film_isocenter[1]/2)+3, fill='red')

                    Globals.profiles_mark_isocenter_up_down_line.append(up_down_line)
                    Globals.profiles_mark_isocenter_right_left_line.append(right_left_line)
                    Globals.profiles_mark_isocenter_oval.append(oval)
                    mark_isocenter_window.after(500, lambda: mark_isocenter_window.destroy())
                    Globals.profiles_isocenter_check = True
                    if(Globals.profiles_ROI_check):
                        Globals.profiles_done_button.config(state=ACTIVE)
            """
            #def findCoords(event):
            #    Globals.profiles_iscoenter_coords.append([event.x, event.y])
            #    print(event.x, event.y)
            #    mark_isocenter_image_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
            #    if(len(Globals.profiles_iscoenter_coords)==1):
                    mark_isocenter_image_canvas.config(cursor='bottom_side')
                elif(len(Globals.profiles_iscoenter_coords)==2):
                    mark_isocenter_image_canvas.config(cursor='right_side')
                elif(len(Globals.profiles_iscoenter_coords)==3):
                    mark_isocenter_image_canvas.config(cursor='left_side')
                else:
                    x1=Globals.profiles_iscoenter_coords[0][0];y1=Globals.profiles_iscoenter_coords[0][1]
                    x2=Globals.profiles_iscoenter_coords[1][0];y2=Globals.profiles_iscoenter_coords[1][1]
                    x3=Globals.profiles_iscoenter_coords[2][0];y3=Globals.profiles_iscoenter_coords[2][1]
                    x4=Globals.profiles_iscoenter_coords[3][0];y4=Globals.profiles_iscoenter_coords[3][1]

                    if(y1==y2 and y3==y4):
                        messagebox.showerror("Error", "Reference points are not correct. Try again.")
                        mark_isocenter_window.destroy()
                        markIsocenter(img, new_window)
                        return
                    elif(y1==y2):
                        if(x1==x2):
                            messagebox.showerror("Error", "Reference points are not correct. Try again.")
                            mark_isocenter_window.destroy()
                            markIsocenter(img, new_window)
                            return
                        else:
                            a = 0; b=y1
                            if(x3==x4):
                                isocenter = [x3,y1]
                            else:
                                c=(y3-y4)/(x3-x4); d = y3 - c*x3
                                isocenter = [(d-b)/(a-c), b]
                    elif(y3==y4):
                        if(x3==x4):
                            messagebox.showerror("Error", "Reference points are not correct. Try again.")
                            mark_isocenter_window.destroy()
                            markIsocenter(img, new_window)
                            return
                        else:
                            c = 0; d = y3
                            if(x1==x2):
                                isocenter = [x1,y3]
                            else:
                                a = (y1-y2)/(x1-x2); b = y1 - a*x1
                                isocenter = [(d-b)/(a-c), d]
                    else:
                        if(x1==x2 and x3==x4):
                            messagebox.showerror("Error", "Reference points are not correct. Try again.")
                            mark_isocenter_window.destroy()
                            markIsocenter(img, new_window)
                            return
                        elif(x1==x2):
                            c = (y3-y4)/(x3-x4); d = y3 - c*x3
                            isocenter = [x1, c*x1+d]
                        elif(x3==x4):
                            a = (y1-y2)/(x1-x2); b = y1 - a*x1
                            isocenter = [x3, a*x3+d]
                        else:
                            a = (y1-y2)/(x1-x2)
                            b = y1 - a*x1
                            c = (y3-y4)/(x3-x4)
                            d = y3 - c*x3
                            isocenter = [(d-b)/(a-c), a*(d-b)/(a-c) + b]

                    if(isocenter[0] < 0 or isocenter[1] < 0 or isocenter[0] > 1016 or isocenter[1] > 1270):
                        messagebox.showerror("Error", "Reference points are not correct. Try again.")
                        mark_isocenter_window.destroy()
                        markIsocenter(img, new_window)
                        return
                    
                    Globals.profiles_film_isocenter = isocenter
                    up_down_line = image_canvas.create_line(int(x1/2),int(y1/2),int(x2/2),int(y2/2),fill='purple', smooth=1, width=2)
                    right_left_line = image_canvas.create_line(int(x3/2),int(y3/2),int(x4/2),int(y4/2), fill='purple', smooth=1, width=2)
                    oval = image_canvas.create_oval(int(isocenter[0]/2)-3, int(isocenter[1]/2)-3, int(isocenter[0]/2)+3, \
                        int(isocenter[1]/2)+3, fill='red')

                    Globals.profiles_mark_isocenter_up_down_line.append(up_down_line)
                    Globals.profiles_mark_isocenter_right_left_line.append(right_left_line)
                    Globals.profiles_mark_isocenter_oval.append(oval)
                    mark_isocenter_window.after(500, lambda: mark_isocenter_window.destroy())
                    Globals.profiles_isocenter_check = True
                    if(Globals.profiles_ROI_check):
                        Globals.profiles_done_button.config(state=ACTIVE)
            """    
            mark_isocenter_image_canvas.bind("<Button 1>",findCoords)
            
        mark_isocenter_button_frame = tk.Frame(new_window_scroll_frame)
        mark_isocenter_button_frame.grid(row=3, column=3, padx=(10,10), pady=(0,10))
        mark_isocenter_button_frame.configure(bg='#ffffff')
        new_window_scroll_frame.grid_columnconfigure(2, weight=0)
        new_window_scroll_frame.grid_rowconfigure(2, weight=0)

        mark_isocenter_button = tk.Button(mark_isocenter_button_frame, text='Browse', image=Globals.profiles_mark_isocenter_button_image,\
            cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: markIsocenter(img, new_window))
        mark_isocenter_button.pack(expand=True, fill=BOTH)
        mark_isocenter_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        mark_isocenter_button.image=Globals.profiles_mark_isocenter_button_image

        film_window_mark_ROI_text = tk.Text(new_window_scroll_frame, width=55, height=5)
        film_window_mark_ROI_text.insert(INSERT, \
"When clicking the button \"Mark ROI\" a window showing the\n\
image will appear and you are to drag a rectangle marking \n\
the region of interest. Fidora will assume the film has been\n\
scanned in either portrait or landscape orientation. When\n\
the ROI has been marked it will appear on the image. If you\n\
are not happy with the placement click the button again.")
        film_window_mark_ROI_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_ROI_text.grid(row=4, column=3, rowspan=3, sticky=N+S+E+W, padx=(10,10), pady=(25,0))
        new_window_scroll_frame.grid_columnconfigure(3, weight=0)
        new_window_scroll_frame.grid_rowconfigure(3, weight=0)

        def markROI(img, new_window):
            if(len(Globals.profiles_mark_ROI_rectangle)>0):
                image_canvas.delete(Globals.profiles_mark_ROI_rectangle[0])
                Globals.profiles_mark_ROI_rectangle = []

            Globals.profiles_ROI_coords = []

            img_mark_ROI = ImageTk.PhotoImage(image=img)
            mark_ROI_window = tk.Toplevel(new_window)
            mark_ROI_window.geometry("1035x620+10+10")
            mark_ROI_window.grab_set()

            mark_ROI_over_all_frame = tk.Frame(mark_ROI_window, bd=0, relief=FLAT)
            mark_ROI_over_all_canvas = Canvas(mark_ROI_over_all_frame)

            mark_ROI_xscrollbar = Scrollbar(mark_ROI_over_all_frame, orient=HORIZONTAL, command=mark_ROI_over_all_canvas.xview)
            mark_ROI_yscrollbar = Scrollbar(mark_ROI_over_all_frame, command=mark_ROI_over_all_canvas.yview)

            mark_ROI_scroll_frame = ttk.Frame(mark_ROI_over_all_canvas)
            mark_ROI_scroll_frame.bind("<Configure>", lambda e: mark_ROI_over_all_canvas.configure(scrollregion=mark_ROI_over_all_canvas.bbox('all')))

            mark_ROI_over_all_canvas.create_window((0,0), window=mark_ROI_scroll_frame, anchor='nw')
            mark_ROI_over_all_canvas.configure(xscrollcommand=mark_ROI_xscrollbar.set, yscrollcommand=mark_ROI_yscrollbar.set)

            mark_ROI_over_all_frame.config(highlightthickness=0, bg='#ffffff')
            mark_ROI_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
            mark_ROI_over_all_frame.pack(expand=True, fill=BOTH)
            mark_ROI_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
            mark_ROI_over_all_frame.grid_columnconfigure(0, weight=1)
            mark_ROI_over_all_frame.grid_rowconfigure(0, weight=1)
            mark_ROI_xscrollbar.grid(row=1, column=0, sticky=E+W)
            mark_ROI_over_all_frame.grid_columnconfigure(1, weight=0)
            mark_ROI_over_all_frame.grid_rowconfigure(1, weight=0)
            mark_ROI_yscrollbar.grid(row=0, column=1, sticky=N+S)
            mark_ROI_over_all_frame.grid_columnconfigure(2, weight=0)
            mark_ROI_over_all_frame.grid_rowconfigure(2, weight=0)

            mark_ROI_image_canvas = tk.Canvas(mark_ROI_scroll_frame)
            mark_ROI_image_canvas.grid(row=0,column=0, rowspan=10, columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
            mark_ROI_scroll_frame.grid_columnconfigure(0, weight=0)
            mark_ROI_scroll_frame.grid_rowconfigure(0, weight=0)

            mark_ROI_image_canvas.create_image(0,0,image=img_mark_ROI,anchor="nw")
            mark_ROI_image_canvas.image = img_mark_ROI
            mark_ROI_image_canvas.config(bg='#E5f9ff', relief=FLAT, bd=0, \
                scrollregion=mark_ROI_image_canvas.bbox(ALL), height=img_mark_ROI.height(), width=img_mark_ROI.width())
            mark_ROI_image_canvas.grid_propagate(0)

            rectangle = mark_ROI_image_canvas.create_rectangle(0,0,0,0,outline='green')
            rectangle_top_corner = []
            rectangle_bottom_corner = []
            def buttonPushed(event):
                rectangle_top_corner.append([event.x, event.y])
        
            def buttonMoving(event):
                mark_ROI_image_canvas.coords(rectangle, rectangle_top_corner[0][0], rectangle_top_corner[0][1], \
                event.x, event.y)

            def buttonReleased(event):
                rectangle_bottom_corner.append([event.x, event.y])
                mark_ROI_image_canvas.coords(rectangle, rectangle_top_corner[0][0], rectangle_top_corner[0][1],\
                    rectangle_bottom_corner[0][0], rectangle_bottom_corner[0][1])
                mark_ROI_image_canvas.itemconfig(rectangle, outline='Blue')
                ### Husk at koordinatene går bortover så nedover! Top left - top right - bottom left - bottom right
                Globals.profiles_ROI_coords.append([rectangle_top_corner[0][0], rectangle_top_corner[0][1]])
                Globals.profiles_ROI_coords.append([rectangle_bottom_corner[0][0], rectangle_top_corner[0][1]])
                Globals.profiles_ROI_coords.append([rectangle_top_corner[0][0], rectangle_bottom_corner[0][1]])
                Globals.profiles_ROI_coords.append([rectangle_bottom_corner[0][0], rectangle_bottom_corner[0][1]])

                rect = image_canvas.create_rectangle(int((rectangle_top_corner[0][0])/2), int((rectangle_top_corner[0][1])/2),\
                    int((rectangle_bottom_corner[0][0])/2), int((rectangle_bottom_corner[0][1])/2), outline='Blue', width=2)
                Globals.profiles_mark_ROI_rectangle.append(rect)

                Globals.profiles_ROI_check = True
                if(Globals.profiles_isocenter_check):
                    Globals.profiles_done_button.config(state=ACTIVE)

                mark_ROI_window.after(500, lambda: mark_ROI_window.destroy())

            mark_ROI_image_canvas.bind("<B1-Motion>", buttonMoving)
            mark_ROI_image_canvas.bind("<Button-1>", buttonPushed)
            mark_ROI_image_canvas.bind("<ButtonRelease-1>", buttonReleased)




        mark_ROI_button_frame = tk.Frame(new_window_scroll_frame)
        mark_ROI_button_frame.grid(row=7, column=3, padx=(10,10), pady=(0,5))
        mark_ROI_button_frame.configure(bg='#ffffff')
        new_window_scroll_frame.grid_columnconfigure(4, weight=0)
        new_window_scroll_frame.grid_rowconfigure(4, weight=0)

        mark_ROI_button = tk.Button(mark_ROI_button_frame, text='Browse', image=Globals.profiles_mark_ROI_button_image,\
            cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: markROI(img, new_window))
        mark_ROI_button.pack(expand=True, fill=BOTH)
        mark_ROI_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        mark_ROI_button.image=Globals.profiles_mark_ROI_button_image

        def finishFilmMarkers():
            choose_batch_window = tk.Toplevel(new_window)
            choose_batch_window.geometry("670x380+50+50")
            choose_batch_window.grab_set()

            choose_batch_frame = tk.Frame(choose_batch_window)
            choose_batch_frame.pack(expand=True, fill=BOTH)
            choose_batch_frame.configure(bg='#ffffff')

            batch_cnt = 0
            weight_cnt = 0
            read = open('calibration.txt', 'r')
            lines = read.readlines()
            read.close()
            row_cnt=0
            for l in lines:
                words = l.split()
                line = "Batch nr.  : " + words[2] + ".    Date:   " + words[0] + "  " + words[1] + "."
                write_batch_nr = tk.Text(choose_batch_frame, width=10, height=1)
                write_batch_nr.grid(row=row_cnt, column=0, sticky=N+S+W+E, padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_batch_nr.insert(INSERT, "Batch nr.: ")
                write_batch_nr.config(state=DISABLED, bd = 0, font=('calibri', '12', 'bold'))
                weight_cnt+=1
                write_batch = tk.Text(choose_batch_frame, width=20, height=1)
                write_batch.grid(row=row_cnt, column=1, sticky=N+S+W+E, padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_batch.insert(INSERT, words[2])
                write_batch.config(state=DISABLED, bd = 0, font=('calibri', '12'))
                weight_cnt+=1
                write_batch_date = tk.Text(choose_batch_frame, width=8, height=1)
                write_batch_date.grid(row=row_cnt, column=2, sticky=N+S+W+E, padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_batch_date.insert(INSERT, "Date: ")
                write_batch_date.config(state=DISABLED, bd = 0, font=('calibri', '12', 'bold'))
                weight_cnt+=1
                write_date = tk.Text(choose_batch_frame, width=30, height=1)
                write_date.grid(row=row_cnt, column=3, sticky=N+S+W+E, padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_date.insert(INSERT, words[0] + ", " + words[1] + "")
                write_date.config(state=DISABLED, bd = 0, font=('calibri', '12'))
                weight_cnt+=1

                Radiobutton(choose_batch_frame, text='',bg='#ffffff', cursor='hand2',font=('calibri', '14'), \
                    variable=Globals.profiles_film_batch, value=batch_cnt).grid(row=row_cnt, \
                    column=4, sticky=N+S+W+E, padx=(5,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                weight_cnt+=1;row_cnt+=1;batch_cnt+=1

            def set_batch():
                choose_batch_window.destroy()
                f = open('calibration.txt', 'r')
                lines = f.readlines()
                words = lines[Globals.profiles_film_batch.get()].split()
                Globals.profiles_popt_red[0] = float(words[3])
                Globals.profiles_popt_red[1] = float(words[4])
                Globals.profiles_popt_red[2] = float(words[5])
                f.close()

                Globals.profiles_film_dataset_ROI_red_channel_dose = np.zeros((Globals.profiles_film_dataset_ROI_red_channel.shape[0],\
                    Globals.profiles_film_dataset_ROI_red_channel.shape[1]))
                for i in range(Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0]):
                    for j in range(Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]):
                        Globals.profiles_film_dataset_ROI_red_channel_dose[i,j] = pixel_to_dose(Globals.profiles_film_dataset_ROI_red_channel[i,j], \
                            Globals.profiles_popt_red[0], Globals.profiles_popt_red[1], Globals.profiles_popt_red[2])

                film_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
                film_write_image.image = scaled_image_visual

                mx_film=np.max(Globals.profiles_film_dataset_ROI_red_channel_dose)
                Globals.profiles_max_dose_film = mx_film
                img_film = Globals.profiles_film_dataset_ROI_red_channel_dose
                img_film = img_film/mx_film
                PIL_img_film = Image.fromarray(np.uint8(cm.viridis(img_film)*255))

                scaled_image_visual_film = ImageTk.PhotoImage(image=PIL_img_film)
                film_dose_write_image.create_image(0,0,image=scaled_image_visual_film, anchor="nw")
                film_dose_write_image.image = scaled_image_visual_film

                film_scanned_image_text_canvas.create_image(0,0,image=Globals.profiles_scanned_image_text_image, anchor="nw")
                film_scanned_image_text_canvas.image = Globals.profiles_scanned_image_text_image
                film_dose_map_image_text_canvas.create_image(0,0, image=Globals.profiles_film_dose_map_text_image, anchor="nw")
                film_dose_map_image_text_canvas.image=Globals.profiles_film_dose_map_text_image

                new_window.destroy()

            set_batch_button_frame = tk.Frame(choose_batch_frame)
            set_batch_button_frame.grid(row=row_cnt, column=1, columnspan=3, padx=(10,0), pady=(5,5))
            set_batch_button_frame.configure(bg='#ffffff')
            choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
            choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)

            set_batch_button = tk.Button(set_batch_button_frame, text='OK', image=Globals.done_button_image, cursor='hand2',\
                font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=set_batch)
            set_batch_button.pack(expand=True, fill=BOTH)
            set_batch_button.image=Globals.done_button_image
            
            #def callback_to_closing():
            #    Globals.profiles_film_window.destroy()
            #    Globals.profiles_film_window_open = False
            
            #Globals.profiles_film_window = tk.Toplevel(Globals.tab4_canvas)
            #Globals.profiles_film_window.geometry("600x500+0+0")
            #Globals.profiles_film_window_open = True
            #Globals.profiles_film_window.protocol("WM_DELETE_WINDOW", callback_to_closing)

            #film_window_over_all_frame = tk.Frame(Globals.profiles_film_window, bd=0, relief=FLAT)
            #film_window_over_all_canvas = Canvas(film_window_over_all_frame)
            #film_window_xscrollbar = Scrollbar(film_window_over_all_frame, orient=HORIZONTAL, command=film_window_over_all_canvas.xview)
            #film_window_yscrollbar = Scrollbar(film_window_over_all_frame, command=film_window_over_all_canvas.yview)
            #film_window_scroll_frame = ttk.Frame(film_window_over_all_canvas)
            #film_window_scroll_frame.bind("<Configure>", lambda e: film_window_over_all_canvas.configure(scrollregion=film_window_over_all_canvas.bbox('all')))
            #film_window_over_all_canvas.create_window((0,0), window=film_window_scroll_frame, anchor='nw')
            #film_window_over_all_canvas.configure(xscrollcommand=film_window_xscrollbar.set, yscrollcommand=film_window_yscrollbar.set)

            #film_window_over_all_frame.config(highlightthickness=0, bg='#ffffff')
            #film_window_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
            #film_window_over_all_frame.pack(expand=True, fill=BOTH)
            #film_window_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
            #film_window_over_all_frame.grid_columnconfigure(0, weight=1)
            #film_window_over_all_frame.grid_rowconfigure(0, weight=1)
            #film_window_xscrollbar.grid(row=1, column=0, sticky=E+W)
            #film_window_over_all_frame.grid_columnconfigure(1, weight=0)
            #film_window_over_all_frame.grid_rowconfigure(1, weight=0)
            #film_window_yscrollbar.grid(row=0, column=1, sticky=N+S)
            #film_window_over_all_frame.grid_columnconfigure(2, weight=0)
            #film_window_over_all_frame.grid_rowconfigure(2, weight=0)

            

            img_ROI = Globals.profiles_film_dataset[Globals.profiles_ROI_coords[0][1]:Globals.profiles_ROI_coords[2][1],\
                Globals.profiles_ROI_coords[0][0]:Globals.profiles_ROI_coords[1][0], :]
            img_ROI_red_channel = img_ROI[:,:,2]
            Globals.profiles_film_dataset_ROI = img_ROI
            Globals.profiles_film_dataset_ROI_red_channel = img_ROI_red_channel
            R = img_ROI[:,:,2];B = img_ROI[:,:,0]; G = img_ROI[:,:,1]
            img_ROI_RGB = np.zeros(img_ROI.shape)
            img_ROI_RGB[:,:,0]=R; img_ROI_RGB[:,:,1]=G; img_ROI_RGB[:,:,2]=B 
            PIL_img_ROI = (img_ROI_RGB/256).astype('uint8')
            PIL_img_ROI = Image.fromarray(PIL_img_ROI, 'RGB')
            #PIL_img_ROI = Image.fromarray((img_ROI_RGB * 255).astype(np.uint8), 'RGB')
            wid = PIL_img_ROI.width;heig = PIL_img_ROI.height
            #film_window_write_image = tk.Canvas(film_window_scroll_frame)
            
            film_image_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
            film_image_canvas.grid(row=0,column=0, sticky=N+S+W+E)
            Globals.profiles_film_panedwindow.add(film_image_canvas, \
                height=max(heig,Globals.profiles_scanned_image_text_image.height()), \
                    width=wid + Globals.profiles_scanned_image_text_image.width())
            film_image_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
                height=max(heig,Globals.profiles_scanned_image_text_image.height()), \
                    width=wid + Globals.profiles_scanned_image_text_image.width())

            film_write_image = tk.Canvas(film_image_canvas)
            film_write_image.grid(row=0,column=1,sticky=N+S+W+E)
            film_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)
            #film_window_write_image.pack(expand=True, fill=BOTH)
            #film_window_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

            film_dose_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
            film_dose_canvas.grid(row=1,column=0, sticky=N+S+W+E)
            Globals.profiles_film_panedwindow.add(film_dose_canvas, \
                height=max(heig,Globals.profiles_film_dose_map_text_image.height()), \
                    width=wid + Globals.profiles_film_dose_map_text_image.width())
            film_dose_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
                height=max(heig,Globals.profiles_film_dose_map_text_image.height()), \
                    width=wid + Globals.profiles_film_dose_map_text_image.width())
            
            film_dose_write_image = tk.Canvas(film_dose_canvas)
            film_dose_write_image.grid(row=0,column=1,sticky=N+S+W+E)
            film_dose_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

            film_scanned_image_text_canvas=tk.Canvas(film_image_canvas)
            film_scanned_image_text_canvas.grid(row=0,column=0,sticky=N+S+W+E)
            film_scanned_image_text_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
                height=Globals.profiles_scanned_image_text_image.height(), width=Globals.profiles_scanned_image_text_image.width())

            film_dose_map_image_text_canvas=tk.Canvas(film_dose_canvas)
            film_dose_map_image_text_canvas.grid(row=0,column=0,sticky=N+S+W+E)
            film_dose_map_image_text_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
                height=Globals.profiles_film_dose_map_text_image.height(), width=Globals.profiles_film_dose_map_text_image.width())

            scaled_image_visual = PIL_img_ROI
            scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
            
            #film_window_write_image.create_image(0,0,image=scaled_image_visual,anchor="nw")
            #film_window_write_image.image = scaled_image_visual

            Globals.profiles_upload_button_doseplan.config(state=ACTIVE)
            Globals.profiles_upload_button_rtplan.config(state=ACTIVE)
            Globals.profiles_upload_button_film.config(state=DISABLED)

            #Beregne avstand mellom ROI og isocenter gitt i mm 
            # [top left[mot venstre, oppover], top right[mot venstre (høyre blir negativ), oppover], bottom left, bottom right]
            Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0]-Globals.profiles_ROI_coords[0][0])*0.2, \
                (Globals.profiles_film_isocenter[1] -Globals.profiles_ROI_coords[0][1])*0.2])
            Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0] - Globals.profiles_ROI_coords[1][0])*0.2,\
                (Globals.profiles_film_isocenter[1] - Globals.profiles_ROI_coords[1][1])*0.2])
            Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0] - Globals.profiles_ROI_coords[2][0])*0.2,\
                (Globals.profiles_film_isocenter[1] - Globals.profiles_ROI_coords[2][1])*0.2])
            Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0] - Globals.profiles_ROI_coords[3][0])*0.2,\
                (Globals.profiles_film_isocenter[1] - Globals.profiles_ROI_coords[3][1])*0.2])

            
        done_button_frame = tk.Frame(new_window_scroll_frame)
        done_button_frame.grid(row=9, column=3, padx=(10,10), pady=(5,5))
        done_button_frame.configure(bg='#ffffff')
        new_window_scroll_frame.grid_columnconfigure(5, weight=0)
        new_window_scroll_frame.grid_rowconfigure(5, weight=0)

        Globals.profiles_done_button = tk.Button(done_button_frame, text='Done', image=Globals.done_button_image,\
            cursor='hand2', font=('calibri', '14'), relief=FLAT, state=DISABLED, command=finishFilmMarkers)
        Globals.profiles_done_button.pack(expand=True, fill=BOTH)
        Globals.profiles_done_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        Globals.profiles_done_button.image=Globals.done_button_image


    elif(ext==""):
        return 
    else:
        messagebox.showerror("Error", "The file must be a *.tif file")

def plot_profiles():
    #print(Globals.profiles_film_orientation.get())
    return


def help_showPlanes():
    new_window = tk.Toplevel(Globals.tab4)
    w = Globals.profiles_showPlanes_image.width()
    h = Globals.profiles_showPlanes_image.height()
    new_window.geometry("%dx%d+0+0" % (w, h))
    new_window.grab_set()

    canvas = tk.Canvas(new_window)
    canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    canvas.create_image(0, 0, image=Globals.profiles_showPlanes_image, anchor='nw')
    canvas.pack(expand=True, fill=BOTH)
    


def help_showDepth():
    new_window = tk.Toplevel(Globals.tab4)
    w = Globals.profiles_showDirections_image.width()
    h = Globals.profiles_showDirections_image.height()
    new_window.geometry("%dx%d+0+0" % (w, h))
    new_window.grab_set()

    canvas = tk.Canvas(new_window)
    canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    canvas.create_image(0,0, image=Globals.profiles_showDirections_image, anchor='nw')
    canvas.pack(expand=True, fill=BOTH)
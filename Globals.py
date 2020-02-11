import tkinter as tk
from tkinter import ttk, StringVar, IntVar, Scrollbar, RIGHT, Y
import numpy as np

global form 
form = tk.Tk()

global tab_parent
tab_parent = ttk.Notebook(form)

global intro_tab
intro_tab = ttk.Frame(tab_parent)
global tab1
tab1 = ttk.Frame(tab_parent)
global tab2
tab2 = ttk.Frame(tab_parent)
global tab3
tab3 = ttk.Frame(tab_parent)
global tab4
tab4 = ttk.Frame(tab_parent)

sb = Scrollbar(tab2)
sb.pack(side = RIGHT, fill = Y)

global dose_response_scroll_window_1
dose_response_scroll_window_1 = tk.Canvas(tab2,  yscrollcommand = sb.set, width=200, height=100)
dose_response_scroll_window_1.place(relwidth=0.48, relheight=0.55, relx = 0.5, rely = 0.42)

sb.config(command = dose_response_scroll_window_1.yview )  


global CoMet_dpi
CoMet_dpi = StringVar(tab1)
CoMet_dpi.set("127")

global doseResponse_dpi
doseResponse_dpi=StringVar(tab2)
doseResponse_dpi.set("127")

global CoMet_saveAs
CoMet_saveAs = tk.StringVar(tab1)
CoMet_saveAs.set(".dcm")

global CoMet_uploaded_filename 
CoMet_uploaded_filename=StringVar(tab1)
CoMet_uploaded_filename.set("Error!")

global CoMet_export_folder
CoMet_export_folder=StringVar(tab1)
CoMet_export_folder.set("Error!")

global doseResponse_uploaded_filename 
doseResponse_uploaded_filename=StringVar(tab2)
doseResponse_uploaded_filename.set("Error!")

global CoMet_correcte_image_filename_box

global CoMet_corrected_image_filename          
CoMet_corrected_image_filename=StringVar(tab1)
CoMet_corrected_image_filename.set("Error!")

global CoMet_patientName_box

global CoMet_patientName
CoMet_patientName=StringVar(tab1)
CoMet_patientName.set("Error!")

global CoMet_correctedImage
CoMet_correctedImage=None

global dose_response_var1 
dose_response_var1= IntVar()
dose_response_var1.set(1)

global dose_response_var2
dose_response_var2 = IntVar()
dose_response_var2.set(1)

global dose_response_var3
dose_response_var3 = IntVar()
dose_response_var3.set(1)

global dose_response_var4
dose_response_var4 = IntVar()

global dose_response_var5
dose_response_var5 = IntVar()

global dose_response_uploaded_filenames
dose_response_uploaded_filenames = np.array([])

global dose_response_new_window_countY
dose_response_new_window_countY = 0.2

global avg_red_vector
avg_red_vector = []

global avg_green_vector
avg_green_vector = []

global avg_blue_vector
avg_blue_vector = []

global dose_response_results_coordY
dose_response_results_coordY = 0.35

global dose_response_inOrOut
dose_response_inOrOut = True

global dose_response_delete_buttons
dose_response_delete_buttons = []

global dose_response_red_list
dose_response_red_list = []

global dose_response_green_list
dose_response_green_list = []

global dose_response_blue_list
dose_response_blue_list = []

global dose_response_dose_list
dose_response_dose_list = []

############################### Correction matrix ######################################3

global correction127_red
with open('output_red_127.txt', 'r') as f:
    correction127_red = [[float(num) for num in line.split(',')] for line in f]
correction127_red = np.matrix(correction127_red)
global correction127_green
with open('output_green_127.txt', 'r') as f:
    correction127_green = [[float(num) for num in line.split(',')] for line in f]
correction127_green = np.matrix(correction127_green)

global correction127_blue
with open('output_blue_127.txt', 'r') as f:
    correction127_blue = [[float(num) for num in line.split(',')] for line in f]
correction127_blue = np.matrix(correction127_blue)

global correction72_red
with open('output_red_72.txt', 'r') as f:
    correction72_red = [[float(num) for num in line.split(',')] for line in f]
correction72_red = np.matrix(correction72_red)

global correction72_green
with open('output_green_72.txt', 'r') as f:
    correction72_green = [[float(num) for num in line.split(',')] for line in f]
correction72_green = np.matrix(correction72_green)

global correction72_blue
with open('output_blue_72.txt', 'r') as f:
    correction72_blue = [[float(num) for num in line.split(',')] for line in f]
correction72_blue = np.matrix(correction72_blue)


global correctionMatrix127
correctionMatrix127 = np.zeros((1270,1016,3))
correctionMatrix127[:,:,0] = correction127_blue[:,:]
correctionMatrix127[:,:,1] = correction127_green[:,:]
correctionMatrix127[:,:,2] = correction127_red[:,:]

global correctionMatrix72
correctionMatrix72 = np.zeros((720,576,3))
correctionMatrix72[:,:,0] = correction72_blue[:,:]
correctionMatrix72[:,:,1] = correction72_green[:,:]
correctionMatrix72[:,:,2] = correction72_red[:,:]

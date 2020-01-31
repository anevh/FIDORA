import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, \
    PhotoImage, BOTH, Toplevel, GROOVE, ACTIVE
import cv2
import numpy as np
import os
from os.path import normpath, basename

## Function to do nothing (temp)
def nothingButton():
    return

def UploadAction(new_window, event=None):
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(ext==".tif"):
        Globals.dose_response_uploaded_filenames = np.append(Globals.dose_response_uploaded_filenames, file)
        uploaded_filename = tk.Text(new_window, height=1, width=1)
        uploaded_filename.place(relwidth=0.4, relheight=0.05, \
            relx=0.5, rely=Globals.dose_response_new_window_countY)
        uploaded_filename.insert(INSERT, basename(normpath(file))) 
        uploaded_filename.config(state=DISABLED, bd=0, font=('calibri', '12'))
        Globals.dose_response_new_window_countY+=0.08
    elif(ext==""):
        return 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")
    #print(Globals.dose_response_uploaded_filenames)

def readImage(filename):
    image = cv2.imread(filename, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if(image is None):
        current_folder = os.getcwd()
        #script_path = Globals.CoMet_uploaded_filename.get()
        parent = os.path.dirname(filename)
        os.chdir(parent)
        image=cv2.imread(basename(normpath(filename)), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        os.chdir(current_folder)
    if(image is None):
         messagebox.showerror("Error", "Something has happen. Check that the filename does not contain Æ,Ø,Å")
         return
    
    if(image.shape[2] == 3):
        #if(Globals.doseResponse_dpi.get()=="127" and image.shape[0]==1270 and image.shape[1]==1016):
        if(image.shape[0]==1270 and image.shape[1]==1016):
            image = abs(image-Globals.correctionMatrix127)
        #elif(Globals.doseResponse_dpi.get()=="72" and image.shape[0]==720 and image.shape[1]==576):
        elif(image.shape[0]==720 and image.shape[1]==576):
            image = abs(image - Globals.correctionMatrix72)
        else:
            messagebox.showerror("Error","The resolution of the image is not consistent with dpi:" + Globals.doseResponse_dpi.get())

    else:
        messagebox.showerror("Error","The uploaded image need to be in RGB-format")

    sum_red=0;sum_green=0;sum_blue=0
    if(Globals.doseResponse_dpi.get() == "127"):
        #1270 x 1016
        #635  -  508
        # 622 <-> 647      and      495  <->  520
        
        for i in range(622,647):
            for j in range(495, 520):
                sum_red += image[i,j,2]
                sum_green += image[i,j,1]
                sum_blue += image[i,j,0]
        sum_red = sum_red/(25*25)
        sum_green = sum_green/(25*25)
        sum_blue = sum_blue/(25*25)
        return sum_red, sum_green, sum_blue
    elif(Globals.doseResponse_dpi.get() == "72"):
        #720 x 576
        #360 x 288
        #352 <-> 367     and     280 <-> 295
        
        for i in range(352,367):
            for j in range(280,295):
                sum_red+=image[i,j,2]
                sum_green+=image[i,j,1]
                sum_blue+=image[i,j,0]
        sum_red = sum_red/(15*15)
        sum_green = sum_green/(15*15)
        sum_blue = sum_blue/(15*15)
        return sum_red, sum_green, sum_blue
    else:
        messagebox.showerror("Error", "Something has gone wrong with the doseResponse_dpi")
        return False


## Function to find mean of uploaded images with same dose.
def avgAllFiles(write_dose_box, new_window):

    #First block is to test that everythin is filled in and as expected.
    dose_input = write_dose_box.get("1.0",'end-1c')
    if (dose_input == " "):
        messagebox.showerror("Error", "Input dose")
        return
    try:
        dose_input = float(dose_input)
    except:
        messagebox.showerror("Error","The dose must be a number")
        return
    if(len(Globals.dose_response_uploaded_filenames) == 0):
        messagebox.showerror("Error", "No files uploaded")
        return

    #Calculates the mean in each color channel
    avg_red=0;avg_green=0;avg_blue=0
    for i in range(0, len(Globals.dose_response_uploaded_filenames)):
        if(readImage(Globals.dose_response_uploaded_filenames[i])==False):
            messagebox.showerror("Error", "A mistake has happend in readImage()")
            return
        red, green, blue = readImage(Globals.dose_response_uploaded_filenames[i])
        avg_red+=red
        avg_green+=green
        avg_blue+=blue

    avg_red = avg_red/len(Globals.dose_response_uploaded_filenames)
    avg_green = avg_green/len(Globals.dose_response_uploaded_filenames)
    avg_blue = avg_blue/len(Globals.dose_response_uploaded_filenames)

    Globals.avg_red_vector.append([dose_input, avg_red])
    Globals.avg_green_vector.append([dose_input, avg_green])
    Globals.avg_blue_vector.append([dose_input, avg_blue])

    result_red = tk.Text(Globals.tab2, height=1, width=1)
    result_red.place(relwidt=0.08, relheight=0.04, relx=0.6, rely=Globals.dose_response_results_coordY)
    result_red.insert(INSERT, avg_red)
    result_red.config(state=DISABLED, bd=0, font=('calibri', '12'))

    result_green = tk.Text(Globals.tab2, height=1, width=1)
    result_green.place(relwidt=0.08, relheight=0.04, relx=0.73, rely=Globals.dose_response_results_coordY)
    result_green.insert(INSERT, avg_green)
    result_green.config(state=DISABLED, bd=0, font=('calibri', '12'))

    result_blue = tk.Text(Globals.tab2, height=1, width=1)
    result_blue.place(relwidt=0.08, relheight=0.04, relx=0.86, rely=Globals.dose_response_results_coordY)
    result_blue.insert(INSERT, avg_blue)
    result_blue.config(state=DISABLED, bd=0, font=('calibri', '12'))

    dose_print = tk.Text(Globals.tab2, height=1, width=1)
    dose_print.place(relwidth=0.04, relheight=0.04, relx = 0.53, rely=Globals.dose_response_results_coordY)
    dose_print.insert(INSERT, dose_input)
    dose_print.config(state=DISABLED, bd=0, font=('calibri', '12'))

    Globals.dose_response_results_coordY += 0.07

    Globals.avg_red_vector = sorted(Globals.avg_red_vector,key=lambda l:l[0])
    Globals.avg_green_vector = sorted(Globals.avg_green_vector,key=lambda l:l[0])
    Globals.avg_blue_vector = sorted(Globals.avg_blue_vector,key=lambda l:l[0])
    """
    temp_red = [];temp_green=[], temp_blue=[]
    i = 0
    while(i < len(Globals.avg_red_vector)):
        temp_red = Globals.avg_red_vector[i] #appen
        temp_green= Globals.avg_green_vector[i]
        temp_blue = Globals.avg_blue_vector[i]

        if(avg_red_vector[i][0] == avg_red_vector[i+1][0])
        
    """

    new_window.destroy()

def create_window():
    new_window = tk.Toplevel(Globals.tab2)
    new_window.geometry("800x400")
    new_window.grab_set()
    
    Globals.dose_response_uploaded_filenames = []
    Globals.dose_response_new_window_countY = 0.3

    write_dose_text = tk.Text(new_window, width=1, height=1)
    write_dose_text.place(relwidth=0.07, relheight=0.075, relx=0.4, rely=0.15)
    write_dose_text.insert(INSERT, "Dose: ")
    write_dose_text.config(state=DISABLED, bd=0, font=('calibri', '14'))

   

    write_dose_box = tk.Text(new_window, width=1, height=1)
    write_dose_box.place(relwidt=0.05, relheight=0.075, relx=0.5, rely=0.15)
    write_dose_box.insert(INSERT, " ")
    write_dose_box.config(state=NORMAL, bd=0, font=('calibri', '14'))

    upload_button = tk.Button(new_window, text='Upload file', cursor='hand2', font=('calibri', '20'), highlightthickness=7, \
        overrelief=GROOVE, state=ACTIVE, width=12, command=lambda: UploadAction(new_window))
    upload_button.place(relwidth=0.2, relheight=0.23, relx=0.23, rely=0.26)

    done_button = tk.Button(new_window, text='Done', cursor='hand2', font=('calibri', '20'), highlightthickness=7, \
        overrelief=GROOVE, state=ACTIVE, width=12, command=lambda: avgAllFiles(write_dose_box, new_window))
    done_button.place(relwidth=0.2, relheight=0.23, relx=0.23, rely=0.6)


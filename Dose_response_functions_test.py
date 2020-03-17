import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, \
    PhotoImage, BOTH, Toplevel, GROOVE, ACTIVE, FLAT, N, S, W, E
import cv2
import numpy as np
import os
from os.path import normpath, basename
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.rcParams['text.usetex'] = True #lagt til for å kunne skrive latex i string
from scipy.optimize import curve_fit
from PIL import Image, ImageTk
import sys
from datetime import datetime
import re

## Function to do nothing (temp)
def nothingButton():
    return

def saveCalibration():
    ask_batch_window = tk.Toplevel(Globals.tab2)
    ask_batch_window.geometry("800x400")
    ask_batch_window.grab_set()

    batch_info = tk.Text(ask_batch_window, width=1, height=1)
    batch_info.place(relwidth = 0.8, relheight = 0.5, relx = 0.1, rely =0.1)
    batch_info.insert(INSERT, 'Write the batch number of current GafChromic film:\n\
        (Defaults to -)')
    batch_info.config(state=DISABLED, bd = 0, font=('calibri', '13'))

    batch = tk.Text(ask_batch_window, width=1, height=1)
    batch.place(relwidth = 0.4, relheight = 0.07, relx = 0.2, rely = 0.6)
    batch.insert(INSERT, " ")
    batch.config(state=NORMAL, bd = 3, font=('calibri', '12'))

    def save_batch():
        Globals.dose_response_batch_number= batch.get("1.0",'end-1c')
        if(Globals.dose_response_batch_number == " "):
            Globals.dose_response_batch_number = "-"
            save_batch_button.config(state=DISABLED)
            ask_batch_window.destroy()
        elif(re.match("^[A-Za-z0-9_]*$", (Globals.dose_response_batch_number).lstrip())==None):
            messagebox.showerror("Error","Batch number can only contain letters and/or numbers")
            ask_batch_window.destroy()
            saveCalibration()
            return
        else:
            save_batch_button.config(state=DISABLED)
            ask_batch_window.destroy()

        f = open('calibration.txt', 'r')
        lines = f.readlines()
        f.close()
        string_to_file = str(datetime.now()) + " " + str(Globals.dose_response_batch_number) + " " + \
            str(Globals.popt_red[0]) + " " + str(Globals.popt_red[1]) + " " + str(Globals.popt_red[2]) + "\n"
        if(len(lines) < 5):
            f = open('calibration.txt', 'a')
            f.write(string_to_file)
            f.close()
        else:
            new_lines = [lines[1], lines[2], lines[3], lines[4], string_to_file]
            f = open('calibration.txt', 'w')
            for i in range(len(new_lines)):
                f.write(new_lines[i])
            f.close()

    save_batch_button = tk.Button(ask_batch_window, text='Save', cursor='hand2',font=('calibri', '13'),\
        highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=save_batch)
    save_batch_button.place(relwidth=0.2, relheight=0.1, relx=0.5, rely=0.55)

    
    Globals.dose_response_save_calibration_button.config(state=DISABLED)


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


def plot_dose_response():

    temp_dose = [item[0] for item in Globals.avg_red_vector]
    temp_avg_red = [item[1] for item in Globals.avg_red_vector]
    temp_avg_green = [item[1] for item in Globals.avg_green_vector]
    temp_avg_blue = [item[1] for item in Globals.avg_blue_vector]
    
    fig = Figure(figsize=(4,3))
    a = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=Globals.dose_response_plot_frame)
    canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+S+E)#grid(row=1, column=0, rowspan=4, columnspan=3, sticky=N+S+E+W, pady=(5,5), padx=(5,5))
    #Globals.tab2_canvas.grid_columnconfigure(9, weight=0)
    #Globals.tab2_canvas.grid_rowconfigure(9, weight=0)
    if(Globals.dose_response_var1.get()):
        a.plot(temp_dose,temp_avg_red, 'ro')
    if(Globals.dose_response_var2.get()):
        a.plot(temp_dose, temp_avg_green, 'g^')
    if(Globals.dose_response_var3.get()):
        a.plot(temp_dose, temp_avg_blue, 'bs')
    #a.plot(xdata, ydata, color='red')
    #a.plot(p, range(2 +max(x)),color='blue')
    
    #a.invert_yaxis()
    ### Får ofte optimaliseringsproblemer..
    if(len(temp_avg_red) > 3):
        Globals.dose_response_save_calibration_button.config(state=ACTIVE)
        sorted_temp_red = sorted(Globals.avg_red_vector,key=lambda l:l[0])
        sorted_temp_avg_red = [item[1] for item in sorted_temp_red]
        sorted_temp_dose = [item[0] for item in sorted_temp_red]

        sorted_temp_green = sorted(Globals.avg_green_vector, key=lambda l:l[0])
        sorted_temp_avg_green = [item[1] for item in sorted_temp_green]
    
        sorted_temp_blue = sorted(Globals.avg_blue_vector, key=lambda l:l[0])
        sorted_temp_avg_blue = [item[1] for item in sorted_temp_blue]

        Globals.popt_red, pcov_red = curve_fit(fitted_dose_response, sorted_temp_dose, sorted_temp_avg_red, p0=[1700, 15172069, -390], maxfev=10000)
        popt_green, pcov_green = curve_fit(fitted_dose_response, sorted_temp_dose, sorted_temp_avg_green, p0=[1700, 15172069, -390], maxfev=10000)
        #popt_blue, pcov_blue = curve_fit(fitted_dose_response, sorted_temp_dose, sorted_temp_avg_blue, p0=[1700, 15172069, -390], maxfev=10000)
        xdata = np.linspace(0,600,1001)
        ydata_red = np.zeros(len(xdata));ydata_green=np.zeros(len(xdata))#;ydata_blue=np.zeros(len(xdata))
        for i in range(len(xdata)):
            ydata_red[i] = fitted_dose_response(xdata[i], Globals.popt_red[0], Globals.popt_red[1], Globals.popt_red[2])
            ydata_green[i] = fitted_dose_response(xdata[i], popt_green[0], popt_green[1], popt_green[2])
            #ydata_blue[i] = fitted_dose_response(xdata[i], popt_blue[0], popt_blue[1], popt_blue[2])
        if(Globals.dose_response_var1.get()):
            a.plot(xdata, ydata_red, color='red')
        if(Globals.dose_response_var2.get()):
            a.plot(xdata, ydata_green, color='green')
        if(Globals.dose_response_var3.get()):
            a.plot(sorted_temp_dose, sorted_temp_avg_blue , color='blue')

       ##### testing latex ##########
        def graph(text):
            out_text_function= "Pixel value = " + str(round(Globals.popt_red[0])) + " + " + str(round(Globals.popt_red[1])) + "/(dose - (" + str(round(Globals.popt_red[2])) + "))"
            tmptext = "$"+out_text_function+"$"
            ax.clear()
            ax.text(0.2, 0.6, tmptext, fontsize = 20)  
            canvas.draw()


        widget = Button(Globals.dose_response_equation_frame, text='Display dose reponse equation')
        widget.pack()
        widget.bind('<Button-1>', graph)
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        ax.get_xaxis().set_visible(False) 
        ax.get_yaxis().set_visible(False)

       ######### test over ############
        #out_text_function = "Pixel value = " + str(round(Globals.popt_red[0])) + " + " + str(round(Globals.popt_red[1])) + "/(dose - (" + str(round(Globals.popt_red[2])) + "))"
        write_out_respons_function = tk.Text(Globals.dose_response_equation_frame, height=2, width=20)
        write_out_respons_function.insert(INSERT, out_text_function )
        write_out_respons_function.grid(row=0, column=0, sticky=N+S+W+E, pady=(5,5), padx=(5,5))
        Globals.dose_response_equation_frame.grid_columnconfigure(0, weight=0)
        Globals.dose_response_equation_frame.grid_rowconfigure(0, weight=0)
        write_out_respons_function.config(state=DISABLED, bd=0, font=('calibri', '12'), bg='#ffffff')    

    ####
    a.set_title ("Title", fontsize=12)
    a.set_ylabel("Pixel value", fontsize=12)
    a.set_xlabel("Dose", fontsize=12)
    fig.tight_layout()
    
    
    canvas.draw()

    return

def delete_line(delete_button):
    #The button index equals the index in Globals.avg_red_vector etc.
    button_index = Globals.dose_response_delete_buttons.index(delete_button)
    Globals.dose_response_red_list[button_index].config(state=DISABLED, bd=0, font=('calibri', '12', 'overstrike'), bg='#D5D8DC')
    Globals.dose_response_green_list[button_index].config(state=DISABLED, bd=0, font=('calibri', '12', 'overstrike'), bg='#D5D8DC')
    Globals.dose_response_blue_list[button_index].config(state=DISABLED, bd=0, font=('calibri', '12', 'overstrike'), bg='#D5D8DC')
    Globals.dose_response_dose_list[button_index].config(state=DISABLED, bd=0, font=('calibri', '12', 'overstrike'), bg='#D5D8DC')
    Globals.dose_response_delete_buttons[button_index].config(state=DISABLED)
    if(len(Globals.dose_response_delete_buttons) > 1):
        del(Globals.avg_red_vector[button_index])
        del(Globals.avg_green_vector[button_index])
        del(Globals.avg_blue_vector[button_index])
        del(Globals.dose_response_delete_buttons[button_index])
    else:
        Globals.avg_red_vector = []
        Globals.avg_green_vector = []
        Globals.avg_blue_vector = []
        Globals.dose_response_delete_buttons = []
    

    plot_dose_response()

def fitted_dose_response(D, a, b, c):
    return a + b/(D-c)




## Function to find mean of uploaded images with same dose.
def avgAllFiles(write_dose_box, new_window):
    #First block is to test that everything is filled in and as expected.
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

    temp_dose = [item[0] for item in Globals.avg_red_vector]
    try:
        indx = temp_dose.index(dose_input)
        Globals.avg_red_vector[indx][1] = (avg_red + Globals.avg_red_vector[indx][1])/2
        Globals.avg_green_vector[indx][1] = (avg_green + Globals.avg_green_vector[indx][1])/2
        Globals.avg_blue_vector[indx][1] = (avg_blue + Globals.avg_blue_vector[indx][1])/2
       
    except:
        Globals.avg_red_vector.append([dose_input, avg_red])
        Globals.avg_green_vector.append([dose_input, avg_green])
        Globals.avg_blue_vector.append([dose_input, avg_blue])

    
    temp_dose = [item[0] for item in Globals.avg_red_vector]


    result_red = tk.Text(Globals.tab2_canvas_files, height=1, width=7)
    result_red.insert(INSERT, round(avg_red))
    result_red.grid(row=Globals.dose_response_files_row_count, column=1, sticky=N+S+W+E, padx=(0,0))
    Globals.tab2_canvas_files.grid_columnconfigure(Globals.dose_response_files_weightcount, weight=0)
    Globals.tab2_canvas_files.grid_rowconfigure(Globals.dose_response_files_weightcount, weight=0)
    #result_red.place(relwidth=0.1, relheight=0.08, relx=0.3, rely=Globals.dose_response_results_coordY)
    result_red.config(state=DISABLED, bd=0, font=('calibri', '12'))
    Globals.dose_response_red_list.append(result_red)
    Globals.dose_response_files_weightcount+=1

    result_green = tk.Text(Globals.tab2_canvas_files, height=1, width=7)
    result_green.insert(INSERT, round(avg_green))
    result_green.grid(row=Globals.dose_response_files_row_count, column=3, sticky=N+S+W+E, padx=(0,0))
    Globals.tab2_canvas_files.grid_columnconfigure(Globals.dose_response_files_weightcount, weight=0)
    Globals.tab2_canvas_files.grid_rowconfigure(Globals.dose_response_files_weightcount, weight=0)
    #result_green.place(relwidth=0.1, relheight=0.08, relx=0.5, rely=Globals.dose_response_results_coordY)
    result_green.config(state=DISABLED, bd=0, font=('calibri', '12'))
    Globals.dose_response_green_list.append(result_green)
    Globals.dose_response_files_weightcount+=1

    result_blue = tk.Text(Globals.tab2_canvas_files, height=1, width=7)
    result_blue.insert(INSERT, round(avg_blue))
    result_blue.grid(row=Globals.dose_response_files_row_count, column=5, sticky=N+S+W+E, padx=(0,5))
    Globals.tab2_canvas_files.grid_columnconfigure(Globals.dose_response_files_weightcount, weight=0)
    Globals.tab2_canvas_files.grid_rowconfigure(Globals.dose_response_files_weightcount, weight=0)
    #result_blue.place(relwidth=0.1, relheight=0.08, relx=0.75, rely=Globals.dose_response_results_coordY)
    result_blue.config(state=DISABLED, bd=0, font=('calibri', '12'))
    Globals.dose_response_blue_list.append(result_blue)
    Globals.dose_response_files_weightcount+=1

    dose_print = tk.Text(Globals.tab2_canvas_files, height=1, width=10)
    dose_print.insert(INSERT, dose_input)
    dose_print.grid(row=Globals.dose_response_files_row_count, column=0, sticky=N+S+W+E, padx=(0,15))
    Globals.tab2_canvas_files.grid_columnconfigure(Globals.dose_response_files_weightcount, weight=0)
    Globals.tab2_canvas_files.grid_rowconfigure(Globals.dose_response_files_weightcount, weight=0)
    #dose_print.place(relwidth=0.15, relheight=0.08, relx = 0.05, rely=Globals.dose_response_results_coordY)
    dose_print.config(state=DISABLED, bd=0, font=('calibri', '12'))
    Globals.dose_response_dose_list.append(dose_print)
    Globals.dose_response_files_weightcount+=1

    path = os.path.dirname(sys.argv[0])
    path = path + "\delete.png"
    img = ImageTk.PhotoImage(file=path)

    delete_button = tk.Button(Globals.tab2_canvas_files, text='Remove', image=img, cursor='hand2',font=('calibri', '18'),\
        highlightthickness= 0, relief=FLAT, state=ACTIVE, width = 15, command=lambda: delete_line(delete_button)) 
    delete_button.image = img
    Globals.dose_response_delete_buttons.append(delete_button)
    delete_button.grid(row=Globals.dose_response_files_row_count, column=7, sticky=N+S+W+E, padx=(5,5))
    Globals.tab2_canvas_files.grid_columnconfigure(Globals.dose_response_files_weightcount, weight=0)
    Globals.tab2_canvas_files.grid_rowconfigure(Globals.dose_response_files_weightcount, weight=0)
    #delete_button.place(relwidth=0.06, relheight=0.06, relx=0.9, rely=Globals.dose_response_results_coordY)
    #Globals.dose_response_results_coordY += 0.1
    Globals.dose_response_files_row_count+=1
    Globals.dose_response_files_weightcount+=1

    plot_dose_response()
    new_window.destroy()

def create_window():
    new_window = tk.Toplevel(Globals.tab2)
    new_window.geometry("800x400")
    new_window.grab_set()
    
    Globals.dose_response_uploaded_filenames = []
    Globals.dose_response_new_window_countY = 0.3

    write_dose_text = tk.Text(new_window, width=1, height=1)
    write_dose_text.place(relwidth=0.11, relheight=0.075, relx=0.36, rely=0.15)
    write_dose_text.insert(INSERT, "Dose (cGy): ")
    write_dose_text.config(state=DISABLED, bd=0, font=('calibri', '14'))

   

    write_dose_box = tk.Text(new_window, width=1, height=1)
    write_dose_box.place(relwidt=0.05, relheight=0.075, relx=0.5, rely=0.15)
    write_dose_box.insert(INSERT, " ")
    write_dose_box.config(state=NORMAL, bd=0, font=('calibri', '14'))

    upload_button = tk.Button(new_window, text='Upload file', cursor='hand2', font=('calibri', '20'), highlightthickness=7, \
        overrelief=GROOVE, state=ACTIVE, width=12, command=lambda: UploadAction(new_window))
    upload_button.place(relwidth=0.2, relheight=0.23, relx=0.23, rely=0.26)

    Globals.dose_response_inOrOut = True
    done_button = tk.Button(new_window, text='Done', cursor='hand2', font=('calibri', '20'), highlightthickness=7, \
        overrelief=GROOVE, state=ACTIVE, width=12, command=lambda: avgAllFiles(write_dose_box, new_window))
    done_button.place(relwidth=0.2, relheight=0.23, relx=0.23, rely=0.6)


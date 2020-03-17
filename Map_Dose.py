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

def dose_to_pixel(D,a,b,c):
    return a + b/(D-c)

def pixel_to_dose(P,a,b,c):
    return c + b/(P-a)

def calculate_dose_map(cv2Img):
    wid = Globals.map_dose_ROI_x_end.get() - Globals.map_dose_ROI_x_start.get()
    heig = Globals.map_dose_ROI_y_end.get() - Globals.map_dose_ROI_y_start.get()
    print(wid, heig)
    doseMap_film = np.zeros((heig, wid))
    for i in range(heig):
        for j in range(wid):
            doseMap_film[i,j] = pixel_to_dose(cv2Img[Globals.map_dose_ROI_y_start.get()+i,Globals.map_dose_ROI_x_start.get()+j,2], \
                Globals.popt_red[0], Globals.popt_red[1], Globals.popt_red[2])
    

    
    fig = Figure(figsize=(0.8,0.8))
    a = fig.add_subplot(111)
    plot_image = a.pcolormesh(doseMap_film, cmap='hsv', rasterized=True, vmin=0, vmax=600)
    fig.colorbar(plot_image, ax=a)
    canvas_dosemap_film = FigureCanvasTkAgg(fig,master = Globals.tab3)
    canvas_dosemap_film.get_tk_widget().place(relwidth=0.3, relheight=0.55, relx = 0.03, rely=0.1)
    canvas_dosemap_film.draw()
    #plotte dosekartet (dette må være krympet (408,508))


def prepare_Image():
    cv2Img = cv2.imread(Globals.map_dose_film_dataset.get(), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if(cv2Img is None):
        current_folder = os.getcwd()
        parent = os.path.dirname(Globals.map_dose_film_dataset.get())
        os.chdir(parent)
        cv2Img=cv2.imread(basename(normpath(Globals.map_dose_film_dataset.get())), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        os.chdir(current_folder)
    if(cv2Img is None):
         messagebox.showerror("Error", "Something has happen. Check that the filename does not contain Æ,Ø,Å")
         return
    
    if(cv2Img.shape[2] == 3):
        if(cv2Img.shape[0]==1270 and cv2Img.shape[1]==1016):
            cv2Img = abs(cv2Img-Globals.correctionMatrix127)
        elif(cv2Img.shape[0]==720 and cv2Img.shape[1]==576):
            cv2Img = abs(cv2Img - Globals.correctionMatrix72)
        else:
            messagebox.showerror("Error","The resolution of the image is not consistent with dpi")

    else:
        messagebox.showerror("Error","The uploaded image need to be in RGB-format")
        return

    #Read last calibration done, or ask if one wish to change
    choose_batch_window = tk.Toplevel(Globals.tab3)
    choose_batch_window.geometry("800x400")
    choose_batch_window.grab_set()

    def set_batch():
        choose_batch_window.destroy()
        f = open('calibration.txt', 'r')
        lines = f.readlines()
        words = lines[Globals.map_dose_film_batch.get()].split()
        Globals.popt_red[0] = float(words[3])
        Globals.popt_red[1] = float(words[4])
        Globals.popt_red[2] = float(words[5])
        f.close()
        calculate_dose_map(cv2Img)

    batch_cnt = 0
    r = open('calibration.txt', 'r')
    lines = r.readlines()
    write_batch_y_coord = 0.3
    for l in lines:
        words = l.split()
        line = "Batch nr.  : " + words[2] + ".    Date:   " + words[0] + "  " + words[1] + "."
        write_batch = tk.Text(choose_batch_window, width=1, height=1)
        write_batch.place(relwidth=0.7, relheight=0.1, relx = 0.1, rely=write_batch_y_coord)
        write_batch.insert(INSERT, line)
        write_batch.config(state=DISABLED, bd = 0, font=('calibri', '12'))
     
        Radiobutton(choose_batch_window, text='',cursor='hand2',font=('calibri', '14'), \
            variable=Globals.map_dose_film_batch, value=batch_cnt).place(relwidth=0.08, \
                relheight=0.1, relx=0.8, rely=write_batch_y_coord)

        write_batch_y_coord+=0.1; batch_cnt+=1

    ok_batch_button = tk.Button(choose_batch_window, text='OK', cursor='hand2',\
        font=('calibri', '14'), overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=set_batch)
    ok_batch_button.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.9)
    r.close()

def draw_ROI(img, scale_horizontal, scale_vertical):
    draw_ROI_window = tk.Toplevel(Globals.tab3)
    draw_ROI_window.grab_set()
    local_frame= Frame(draw_ROI_window, bd = 2, relief=SUNKEN)
    local_frame.grid_rowconfigure(0,weight=1)
    local_frame.grid_columnconfigure(0, weight=1)

    local_canvas = Canvas(local_frame, bd=0)
    local_canvas.grid(row=0,column=0, sticky=N+S+E+W)

    w = 10 + img.width()
    h = 10 + img.height()
    draw_ROI_window.geometry("%dx%d+0+0" % (w, h))

    local_canvas.create_image(0,0,image=img,anchor="nw")
    local_canvas.config(scrollregion=local_canvas.bbox(ALL), cursor='arrow')
    local_canvas.image= img
    
    rectangle = local_canvas.create_rectangle(0,0,0,0,outline='green')

    def buttonPushed(event):
        Globals.map_dose_ROI_x_start.set(event.x)
        Globals.map_dose_ROI_y_start.set(event.y)
        
    def buttonMoving(event):
        local_canvas.coords(rectangle, Globals.map_dose_ROI_x_start.get(), Globals.map_dose_ROI_y_start.get(), \
            event.x, event.y)

    def buttonReleased(event):
        Globals.map_dose_ROI_x_end.set(event.x)
        Globals.map_dose_ROI_y_end.set(event.y)
        local_canvas.coords(rectangle, Globals.map_dose_ROI_x_start.get(), Globals.map_dose_ROI_y_start.get(),\
            Globals.map_dose_ROI_x_end.get(), Globals.map_dose_ROI_y_end.get())
        local_canvas.itemconfig(rectangle, outline='Blue')
        answer = messagebox.askquestion("Question","Happy with placement?", parent=draw_ROI_window)
        if(answer=='yes'):
            Globals.map_dose_ROI_x_start.set(Globals.map_dose_ROI_x_start.get()*scale_horizontal)
            Globals.map_dose_ROI_y_start.set(Globals.map_dose_ROI_y_start.get()*scale_vertical)
            Globals.map_dose_ROI_x_end.set(Globals.map_dose_ROI_x_end.get()*scale_horizontal)
            Globals.map_dose_ROI_y_end.set(Globals.map_dose_ROI_y_end.get()*scale_vertical)
            prepare_Image()
            draw_ROI_window.destroy()
    
    local_canvas.bind("<B1-Motion>", buttonMoving)
    local_canvas.bind("<Button-1>", buttonPushed)
    local_canvas.bind("<ButtonRelease-1>", buttonReleased)

    local_frame.pack(fill='both', expand=1)
    

def draw_image_with_marks(img, scale_horizontal, scale_vertical, mark_isocenter_window, frame):
    #check_isocenter_window = tk.Toplevel(Globals.tab3)
    #check_isocenter_window.grab_set()
    #frame_local = Frame(mark_isocenter_window, bd=2, relief=SUNKEN) #check_isocenter_window, bd=2, relief=SUNKEN)
    #frame_local.grid_rowconfigure(0, weight=1)
    #frame_local.grid_columnconfigure(0, weight=1)
    canvas_local = Canvas(frame, bd=0)
    canvas_local.grid(row=0, column=0, sticky=N+S+E+W)

    #w = 10 + img.width()
    #h = 10 + img.height()
    #check_isocenter_window.geometry("%dx%d+0+0" % (w, h))

    canvas_local.create_image(0,0,image=img,anchor="nw")
    canvas_local.config(scrollregion=canvas_local.bbox(ALL), cursor='arrow')
    canvas_local.image= img
    canvas_local.create_oval(Globals.map_dose_isocenter_map_x_coord_unscaled[0]-2, Globals.map_dose_isocenter_map_y_coord_unscaled[0]-2,\
        Globals.map_dose_isocenter_map_x_coord_unscaled[0]+2, Globals.map_dose_isocenter_map_y_coord_unscaled[0]+2, fill='red')
    canvas_local.create_oval(Globals.map_dose_isocenter_map_x_coord_unscaled[1]-2, Globals.map_dose_isocenter_map_y_coord_unscaled[1]-2, \
        Globals.map_dose_isocenter_map_x_coord_unscaled[1]+2, Globals.map_dose_isocenter_map_y_coord_unscaled[1]+2, fill='red')
    canvas_local.create_oval(Globals.map_dose_isocenter_map_x_coord_unscaled[2]-2, Globals.map_dose_isocenter_map_y_coord_unscaled[2]-2,\
        Globals.map_dose_isocenter_map_x_coord_unscaled[2]+2, Globals.map_dose_isocenter_map_y_coord_unscaled[2]+2, fill='red')
    canvas_local.create_oval(Globals.map_dose_isocenter_map_x_coord_unscaled[3]-2, Globals.map_dose_isocenter_map_y_coord_unscaled[3]-2,\
        Globals.map_dose_isocenter_map_x_coord_unscaled[3]+2, Globals.map_dose_isocenter_map_y_coord_unscaled[3]+2, fill='red')
    
    canvas_local.create_line(Globals.map_dose_isocenter_map_x_coord_unscaled[0], Globals.map_dose_isocenter_map_y_coord_unscaled[0]\
        , Globals.map_dose_isocenter_map_x_coord_unscaled[1], Globals.map_dose_isocenter_map_y_coord_unscaled[1], \
            fill='purple', smooth=1, width=2)
    canvas_local.create_line(Globals.map_dose_isocenter_map_x_coord_unscaled[2], Globals.map_dose_isocenter_map_y_coord_unscaled[2]\
        , Globals.map_dose_isocenter_map_x_coord_unscaled[3], Globals.map_dose_isocenter_map_y_coord_unscaled[3], \
            fill='purple', smooth=1, width=2)

    x1 = Globals.map_dose_isocenter_map_x_coord_unscaled[0]
    x2 = Globals.map_dose_isocenter_map_x_coord_unscaled[1]
    x3 = Globals.map_dose_isocenter_map_x_coord_unscaled[2]
    x4 = Globals.map_dose_isocenter_map_x_coord_unscaled[3]
    y1 = Globals.map_dose_isocenter_map_y_coord_unscaled[0]
    y2 = Globals.map_dose_isocenter_map_y_coord_unscaled[1]
    y3 = Globals.map_dose_isocenter_map_y_coord_unscaled[2]
    y4 = Globals.map_dose_isocenter_map_y_coord_unscaled[3]

   

    if(y1==y2 and y3==y4):
        messagebox.showerror("Error", "Reference points are not correct. Try again.")
        check_isocenter_window.destroy()
        upload_film_data()
    elif(y1==y2):
        if(x1==x2):
            messagebox.showerror("Error", "Reference points are not correct. Try again.")
            check_isocenter_window.destroy()
            upload_film_data()
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
            check_isocenter_window.destroy()
            upload_film_data()
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
            check_isocenter_window.destroy()
            upload_film_data()
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

    #frame.pack(fill='both', expand=1)
    if(isocenter[0] < 0 or isocenter[1] < 0 or isocenter[0] > 408 or isocenter[1] > 508):
        messagebox.showerror("Error", "Reference points are not correct. Try again.")
        mark_isocenter_window.destroy() #check_isocenter_window.destroy()
        upload_film_data()
    else:
        canvas_local.create_oval(isocenter[0]-6, isocenter[1]-6, isocenter[0]+6,isocenter[1]+6, outline="pink") 
        answer = messagebox.askquestion("Question","Happy with placement?", parent=mark_isocenter_window)#check_isocenter_window)
        if(answer=="yes"):
            Globals.map_dose_isocenter_film = [isocenter[0]*scale_horizontal, isocenter[1]*scale_vertical]
            mark_isocenter_window.destroy() #check_isocenter_window.destroy()
            draw_ROI(img, scale_horizontal, scale_vertical)
       
        else:
            mark_isocenter_window.destroy() #check_isocenter_window.destroy()
            upload_film_data()  
            return
    
    



        

def upload_film_data():
    current_folder = os.getcwd()
    os.chdir(os.path.dirname(sys.argv[0]))
    img = Image.open(Globals.map_dose_film_dataset.get())
    if(not (img.width == 1016 or img.width == 576)):
        messagebox.showerror("Error", "Dpi in image has to be 127 or 72")
        return

    Globals.map_dose_isocenter_map_x_coord_scaled = []
    Globals.map_dose_isocenter_map_x_coord_unscaled = []
    Globals.map_dose_isocenter_map_y_coord_scaled = []
    Globals.map_dose_isocenter_map_y_coord_unscaled = []

    mark_isocenter_window = tk.Toplevel(Globals.tab3)
    mark_isocenter_window.grab_set()
    frame = Frame(mark_isocenter_window, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    canvas = Canvas(frame, bd=0)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)

    
    scale_horizontal = img.width/408
    scale_vertical = img.height/508
    img = img.resize((408,508))
    img = ImageTk.PhotoImage(image=img)
    os.chdir(current_folder)
    canvas.image = img

    w = 10 + img.width()
    h = 10 + img.height()
    mark_isocenter_window.geometry("%dx%d+0+0" % (w, h))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL), cursor='sb_up_arrow')
    #x_coor = []
    #y_coor = []
    
    def findCoords(event):
        Globals.map_dose_isocenter_map_x_coord_scaled.append(event.x*scale_vertical)
        Globals.map_dose_isocenter_map_y_coord_scaled.append(event.y*scale_horizontal)
        Globals.map_dose_isocenter_map_x_coord_unscaled.append(event.x)
        Globals.map_dose_isocenter_map_y_coord_unscaled.append(event.y)
        canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        if (len(Globals.map_dose_isocenter_map_x_coord_scaled)==1):
            canvas.config(cursor='sb_down_arrow')
        elif(len(Globals.map_dose_isocenter_map_x_coord_scaled)==2):
            canvas.config(cursor='sb_right_arrow')
        elif(len(Globals.map_dose_isocenter_map_x_coord_scaled)==3):
            canvas.config(cursor='sb_left_arrow')
        else:
            #mark_isocenter_window.destroy()
            draw_image_with_marks(img, scale_horizontal, scale_vertical, mark_isocenter_window, frame)
            
    
    
    canvas.bind("<Button 1>",findCoords)
    frame.pack(fill='both', expand=1)

def UploadAction(type, event=None):
    if(type == "FILM"):
        if(Globals.popt_red[0]==1):
            messagebox.showerror("Error", "No calibration has been found. To a calibration first.")
            return
        Globals.map_dose_film_dataset.set(filedialog.askopenfilename())
        ext = os.path.splitext(Globals.map_dose_film_dataset.get())[-1].lower()
        if(ext==".tif"):
            upload_film_data()
            return
        elif(ext==""):
            Globals.map_dose_film_dataset.set("Error!") 
        else:
            messagebox.showerror("Error", "The file must be a .tif file")
            Globals.map_dose_film_dataset.set("Error!") 


#laste opp bilde og markere i bildene, egen funksjon
#gammatest, lese opp på det og implementere
#Eksportere figurer og dataset ut av programmet
#må lagre siste kalibrering (spørre hvilken kalibrering bruker vil bruke)
# hvordan er doseplanene lagret.
#Endre geometrien slik at den passer alle skjermer. Kan man bruke skjermstørrelsen i en algoritme?


# Laste opp doseplan (for nå er det en enkel matrise, selvkonstruert.)
# laste opp skannet film, korriger automatisk.
# brukeren spesifiserse posisjon på film
# gjøre film om til dose map (bruke dose response)
# tegne dose plan og dose map fra film
# regne gamma
# tegne gamma pass/fail og variasjoner
# skriv ut all info vi får fra gammatest

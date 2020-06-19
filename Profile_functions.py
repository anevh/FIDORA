import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
    PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE, ACTIVE, \
    FLAT, END, Scrollbar, HORIZONTAL, VERTICAL, ttk, TOP, RIGHT, LEFT, ttk
import os
from os.path import normpath, basename
from PIL import Image, ImageTk
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import pydicom
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
import numpy as np


#Bresenham's line algorithm

def clearAll():
    Globals.profiles_film_orientation.set('-')
    Globals.profiles_film_orientation_menu.config(state=ACTIVE, bg = '#ffffff', width=15, relief=FLAT)
    
    #Globals.profiles_depth.config(state=NORMAL, fg='black')
    #Globals.profiles_depth.delete('1.0', END)
    #Globals.profiles_depth.insert(INSERT, " ")

    Globals.profiles_iscoenter_coords = []
    Globals.profiles_film_isocenter = None
    Globals.profiles_film_reference_point = None
    Globals.profiles_mark_isocenter_up_down_line = []
    Globals.profiles_mark_isocenter_right_left_line = []
    Globals.profiles_mark_isocenter_oval = []
    Globals.profiles_mark_reference_point_oval = []
    Globals.profiles_mark_ROI_rectangle = []
    Globals.profiles_ROI_coords = []


    #if(Globals.profiles_isocenter_check and Globals.profiles_ROI_check):
    #    Globals.profiles_done_button.config(state=DISABLED)
    Globals.profiles_isocenter_check = False
    Globals.profiles_ROI_check = False
    Globals.profiles_reference_point_check = False
    Globals.profiles_ROI_reference_point_check = False
    
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
    Globals.profiles_isocenter_mm = None
    Globals.profiles_test_if_added_rtplan = False
    Globals.profiles_test_if_added_doseplan = False

    Globals.tab4_canvas.unbind("<Up>")
    Globals.tab4_canvas.unbind("<Down>")


    return

def getCoordsInRandomLine(x1,y1,x2,y2):
    points = []
    issteep = abs(y2-y1) - abs(x2-x1)
    if issteep > 0:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points


def drawProfiles(even):
    if Globals.profiles_choice_of_profile_line_type.get() == 'h' or Globals.profiles_choice_of_profile_line_type.get() == 'v':
        Globals.profiles_lines = []

    if Globals.profiles_dataset_doseplan == None:
        return
   
    Globals.profiles_adjust_button_right.config(state=ACTIVE)
    Globals.profiles_adjust_button_left.config(state=ACTIVE)
    Globals.profiles_adjust_button_down.config(state=ACTIVE)
    Globals.profiles_adjust_button_up.config(state=ACTIVE)
    Globals.profiles_adjust_button_return.config(state=ACTIVE)
        
        
    def draw(line_orient, dataset_film, dataset_doseplan):
        Globals.profile_plot_canvas.delete('all')
        fig= Figure(figsize=(5,3))
        a = fig.add_subplot(111)
        plot_canvas = FigureCanvasTkAgg(fig, master=Globals.profile_plot_canvas)
        plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+E+W+S, padx=(5,0), pady=(0,0))
        #annotation = a.annotate("HEI", xy=(0,0), xytext=(0,20))
        #annotation.set_visible(False)
        #txt = tk.Text(Globals.profile_plot_canvas, width=50, height=6)
        #txt.insert(INSERT, " ")
        #txt.grid(row=1, column = 1, sticky=N+E+W+S, pady=(5,0), padx=(5,0))  
        #txt.config(bg='#ffffff', font=('calibri', '10'), state=DISABLED, relief=FLAT, bd= 0)
        cols = (' ', 'Point match', 'Distance', 'Dose', 'Rel. to max', 'Rel. to target')
        listBox = ttk.Treeview(Globals.profile_plot_canvas, columns=cols, show='headings')
        for col in cols:
            listBox.heading(col, text=col, anchor=W)
            listBox.column(col ,width=84, stretch=False, anchor=W)    
        listBox.grid(row=1, column=0, columnspan=4)
        lst = [['Film: ', ' ', ' ', ' ', ' ', ' '],\
            ['Doseplan: ', ' ', ' ', ' ', ' ', ' ']]
        for i, (name, m, dis, d, rdROI, rdTarget) in enumerate(lst):
            listBox.insert("", "end", values=(name, m, dis, d, rdROI, rdTarget))
        #a.text(0,0, "", fontsize=7, bbox=dict(facecolor='gray', alpha=0.1))
        #txt.set_visible(False)
        v_line = a.axvline(x=0, ymin=0, ymax=50, c='gray')
        
        #v_line.set_visible(False)

        if line_orient == 'h':
            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                dy = Globals.profiles_doseplan_dataset_ROI.shape[1]/2
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                dy = Globals.profiles_doseplan_dataset_ROI.shape[1]*2/2
            else:
                dy = Globals.profiles_doseplan_dataset_ROI.shape[1]*3/2
            dx = dataset_film.shape[1]*0.2/2
            x = np.linspace(-dx,dx, dataset_film.shape[1])
            y = np.linspace(-dy,dy, Globals.profiles_doseplan_dataset_ROI.shape[1])
            plot_film = dataset_film[Globals.profiles_coordinate_in_dataset,:]/100
            plot_doseplan = dataset_doseplan[Globals.profiles_coordinate_in_dataset, :]*Globals.profiles_dataset_doseplan.DoseGridScaling
            a.plot(x,plot_film, 'r')
            a.plot(y,plot_doseplan, 'b')
        elif line_orient == 'v':
            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                dy = Globals.profiles_doseplan_dataset_ROI.shape[0]/2
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                dy = Globals.profiles_doseplan_dataset_ROI.shape[0]*2/2
            else:
                dy = Globals.profiles_doseplan_dataset_ROI.shape[0]*3/2
            dx = dataset_film.shape[0]*0.2/2
            x = np.linspace(-dx,dx, dataset_film.shape[0])
            y = np.linspace(-dy,dy, Globals.profiles_doseplan_dataset_ROI.shape[0])
            plot_film = dataset_film[:,Globals.profiles_coordinate_in_dataset]/100
            plot_doseplan = dataset_doseplan[:, Globals.profiles_coordinate_in_dataset]*Globals.profiles_dataset_doseplan.DoseGridScaling  #Globals.profiles_doseplan_dataset_ROI
            a.plot(x,plot_film, 'r')
            a.plot(y,plot_doseplan, 'b')
        elif line_orient == 'd':
            start_f_x, start_f_y = Globals.profiles_line_coords_film[0]
            end_f_x, end_f_y = Globals.end_point
            dx=np.sqrt(((end_f_x-start_f_x)*0.2)**2 + ((end_f_y-start_f_y)*0.2)**2)/2
            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                start_d_x, start_d_y = Globals.profiles_line_coords_doseplan[0]
                end_d_x, end_d_y = Globals.end_point
                end_d_x=end_d_x/5; end_d_y=end_d_y/5
                dy=np.sqrt(((end_d_x-start_d_x))**2 + ((end_d_y-start_d_y))**2)/2
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                start_d_x, start_d_y = Globals.profiles_line_coords_doseplan[0]
                end_d_x, end_d_y = Globals.end_point
                end_d_x=end_d_x/10; end_d_y=end_d_y/10
                dy=np.sqrt(((end_d_x-start_d_x)*2)**2 + ((end_d_y-start_d_y)*2)**2)/2
            else:
                start_d_x, start_d_y = Globals.profiles_line_coords_doseplan[0]
                end_d_x, end_d_y = Globals.end_point
                end_d_x=end_d_x/15; end_d_y=end_d_y/15
                dy=np.sqrt(((end_d_x-start_d_x)*3)**2 + ((end_d_y-start_d_y)*3)**2)/2
            
                
            x = np.linspace(-dx,dx,len(dataset_film))
            y = np.linspace(-dy,dy,len(dataset_doseplan))
            plot_film=dataset_film/100
            plot_doseplan=dataset_doseplan*Globals.profiles_dataset_doseplan.DoseGridScaling
            a.plot(x,plot_film, 'r')
            a.plot(y,plot_doseplan, 'b')

        else:
            messagebox.showerror("Error", "Fatal error. Something has gone wrong, try again \n(Code: draw")
            return

       
        a.legend(('Film', 'Doseplan'))
        a.set_title("Profiles", fontsize=12)
        a.set_ylabel("Dose (Gy)", fontsize=12)
        a.set_xlabel("Distance (mm)", fontsize=12)
        
        def mouseMove(event):
            if event.inaxes == a:
                dist = event.xdata
                idx_film = np.searchsorted(x, dist)
                idx_doseplan = np.searchsorted(y, dist)
                if idx_film == 0:
                    idx_film = 0
                elif idx_film == len(x):
                    idx_film = len(x)-1
                else:
                    if abs(x[idx_film-1]-dist) < abs(x[idx_film]-dist):
                        idx_film = idx_film-1
                    else:
                        idx_film = idx_film
                if idx_doseplan == 0:
                    idx_doseplan = 0
                elif idx_doseplan == len(y):
                    idx_doseplan = len(y)-1
                else:
                    if abs(y[idx_doseplan-1]-dist) < abs(y[idx_doseplan]-dist):
                        idx_doseplan = idx_doseplan-1
                    else:
                        idx_doseplan = idx_doseplan
                
                idx_film = int(np.round(idx_film))
                if idx_film < 0:
                    idx_film = 0
                if idx_film >= len(plot_film):
                    idx_film = len(plot_film) - 1
                #if Globals.profiles_dataset_doseplan.PixelSpacing == [1, 1]:
                #    idx_doseplan = int(np.round(idx_doseplan/1))
                #elif Globals.profiles_dataset_doseplan.PixelSpacing == [2, 2]:
                #    idx_doseplan = int(np.round(idx_doseplan/2))
                ##else:
                #    idx_doseplan = np.round(idx_doseplan/3)
                idx_doseplan = int(np.round(idx_doseplan))
                if idx_doseplan < 0:
                    idx_doseplan = 0
                if idx_doseplan >= len(plot_doseplan):
                    idx_doseplan = len(plot_doseplan) - 1
                
                match_text = "\tGraph match: \t"
                match = str(np.round(min(plot_film[idx_film], plot_doseplan[idx_doseplan])/max(plot_film[idx_film], plot_doseplan[idx_doseplan])*100, 2)) + "\n"
                distance_text = "Distance:\t "
                dose_text = "Dose: \t"
                rel_target_dose_text = "Relative to target dose: \t "
                rel_mx_dose_ROI_text = "Relative to max dose in ROI: \n"
                distance = str(np.round(dist,2)) + "\n"
                film = "FILM:   \t"
                dose_film = str(np.round(plot_film[idx_film],2)) + "\t"
                rel_target_dose_film = str(np.round(100*plot_film[idx_film]/Globals.max_dose_doseplan,2)) + "\t\t\t"
                rel_mx_dose_ROI_film = str(np.round(100*plot_film[idx_film]/np.max(plot_film),2)) + "\n"
                doseplan = "DOSEPLAN:  \t"
                dose_doseplan = str(np.round(plot_doseplan[idx_doseplan],2)) + "\t"
                rel_target_dose_doseplan =  str(np.round(100*plot_doseplan[idx_doseplan]/Globals.max_dose_doseplan,2)) + "\t\t\t"
                rel_mx_dose_ROI_doseplan =  str(np.round(100*plot_doseplan[idx_doseplan]/np.max(plot_doseplan),2))
                notation = match_text + distance_text + dose_text, rel_target_dose_text + rel_mx_dose_ROI_text +\
                    film + dose_film + rel_target_dose_film + rel_mx_dose_ROI_film+\
                        doseplan + dose_doseplan + rel_target_dose_doseplan + rel_mx_dose_ROI_doseplan

                children = listBox.get_children()
                for item in children:
                    listBox.delete(item)
                lst = [['Film: ', match, distance, dose_film, rel_mx_dose_ROI_film, rel_target_dose_film],\
                    ['Doseplan: ', match, distance, dose_doseplan, rel_mx_dose_ROI_doseplan, rel_target_dose_doseplan]]
                for i, (name, m, dis, d, rdROI, rdTarget) in enumerate(lst):
                    listBox.insert("", "end", values=(name, m, dis, d, rdROI, rdTarget))
                y_min = max(plot_film[idx_film], plot_doseplan[idx_doseplan])-0.3*max(np.max(plot_film), np.max(plot_doseplan))
                if y_min < 0:
                    y_min = 0
                y_max = max(plot_film[idx_film], plot_doseplan[idx_doseplan])+0.3*max(np.max(plot_film), np.max(plot_doseplan))
                if y_max > max(np.max(plot_film), np.max(plot_doseplan)):
                    y_max =  max(np.max(plot_film), np.max(plot_doseplan))
                v_line.set_xdata(dist)
                #v_line.set_ylim(y_min,y_max)
                #v_line.set_ymax = y
                #v_line.set_ymax = y_max # = 
                #v_line = a.axvline(x=dist, ymin=0, ymax=40, c='gray')
                v_line.set_visible(True)
                fig.canvas.draw_idle()

                def freezeData(event):
                    fig.canvas.mpl_disconnect(cid)
                    v_line.set_visible(False)
                    fig.canvas.draw_idle()
                    def startData(event):
                        fig.canvas.mpl_disconnect(cid2)
                        fig.canvas.mpl_disconnect(cid3)
                        draw(line_orient, dataset_film, dataset_doseplan)
                        

                    cid3 = fig.canvas.mpl_connect('button_press_event', startData)

                cid2 = fig.canvas.mpl_connect('button_press_event', freezeData)
            else:
                return
        
        cid3 = None
        cid = fig.canvas.mpl_connect('motion_notify_event', mouseMove)
        fig.tight_layout()        


    if even:
        draw('d', Globals.profiles_dataset_film_variable_draw, Globals.profiles_dataset_doesplan_variable_draw)
        return
    

    if(Globals.profiles_choice_of_profile_line_type.get() == 'h' and Globals.profiles_dataset_doseplan.PixelSpacing == [1, 1]):
        dataset_film = np.zeros(\
            (Globals.profiles_doseplan_dataset_ROI.shape[0], Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]))
        for i in range(dataset_film.shape[0]-1):
            dataset_film[i,:] = Globals.profiles_film_dataset_ROI_red_channel_dose[int((i*5)+2),:]
        try:
            dataset_film[dataset_film.shape[0]-1,:] = Globals.profiles_film_dataset_ROI_red_channel_dose[int((dataset_film.shape[0]-1)*5+2), :]
        except:
            dataset_film[dataset_film.shape[0]-1,:] = \
                Globals.profiles_film_dataset_ROI_red_channel_dose[Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0]-1,:]


        line_doseplan = Globals.doseplan_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        line_film_dosemap = Globals.film_dose_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        line_film = Globals.film_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        
        Globals.profiles_lines.append(line_doseplan)
        Globals.profiles_lines.append(line_film_dosemap)
        Globals.profiles_lines.append(line_film)
    
        def up_button_pressed(event):
            temp_x = Globals.doseplan_write_image_var_x - 5
            if(temp_x < 0):
                #Outside the frame
                return
            #inside the frame
            Globals.doseplan_write_image_var_x = temp_x
            Globals.profiles_coordinate_in_dataset = int(temp_x/5)
            Globals.doseplan_write_image.coords(line_doseplan,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_dose_write_image.coords(line_film_dosemap, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_write_image.coords(line_film, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        def down_button_pressed(event):
            temp_x = Globals.doseplan_write_image_var_x + 5
            if(temp_x >= Globals.doseplan_write_image_height):
                #Outside the frame
                return
            #Inside the frame
            Globals.profiles_coordinate_in_dataset = int(temp_x/5)
            Globals.doseplan_write_image_var_x = temp_x
            Globals.doseplan_write_image.coords(line_doseplan,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_dose_write_image.coords(line_film_dosemap,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_write_image.coords(line_film, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)
            

        Globals.form.bind("<Up>", up_button_pressed)
        Globals.form.bind("<Down>", down_button_pressed)

        if Globals.profiles_first_time_in_drawProfiles:
            Globals.profiles_first_time_in_drawProfiles = False
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)
    elif(Globals.profiles_choice_of_profile_line_type.get()=='h' and Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
        dataset_film = np.zeros(\
            (Globals.profiles_doseplan_dataset_ROI.shape[0], Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]))
        for i in range(dataset_film.shape[0]-1):
            dataset_film[i,:] = Globals.profiles_film_dataset_ROI_red_channel_dose[int((i*10)+5),:]
        try:
            dataset_film[dataset_film.shape[0]-1,:] = Globals.profiles_film_dataset_ROI_red_channel_dose[int((dataset_film.shape[0]-1)*10+5), :]
        except:
            dataset_film[dataset_film.shape[0]-1,:] = \
                Globals.profiles_film_dataset_ROI_red_channel_dose[Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0]-1,:]


        line_doseplan = Globals.doseplan_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        line_film_dosemap = Globals.film_dose_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        line_film = Globals.film_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')

        Globals.profiles_lines.append(line_doseplan)
        Globals.profiles_lines.append(line_film_dosemap)
        Globals.profiles_lines.append(line_film)

        def up_button_pressed(event):
            temp_x = Globals.doseplan_write_image_var_x - 10
            if(temp_x < 0):
                #Outside the frame
                return
            #inside the frame
            Globals.doseplan_write_image_var_x = temp_x
            Globals.profiles_coordinate_in_dataset = int(temp_x/10)
            Globals.doseplan_write_image.coords(line_doseplan,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_dose_write_image.coords(line_film_dosemap, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_write_image.coords(line_film, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        def down_button_pressed(event):
            temp_x = Globals.doseplan_write_image_var_x + 10
            if(temp_x >= Globals.doseplan_write_image_height):
                #Outside the frame
                return
            #Inside the frame
            Globals.profiles_coordinate_in_dataset = int(temp_x/10)
            Globals.doseplan_write_image_var_x = temp_x
            Globals.doseplan_write_image.coords(line_doseplan,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_dose_write_image.coords(line_film_dosemap,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_write_image.coords(line_film, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        Globals.form.bind("<Up>", up_button_pressed)
        Globals.form.bind("<Down>", down_button_pressed)

        if Globals.profiles_first_time_in_drawProfiles:
            Globals.profiles_first_time_in_drawProfiles = False
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)

    elif(Globals.profiles_choice_of_profile_line_type.get() == 'h' and Globals.profiles_dataset_doseplan.PixelSpacing==[3, 3]):
        dataset_film = np.zeros(\
            (Globals.profiles_doseplan_dataset_ROI.shape[0], Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]))
        for i in range(dataset_film.shape[0]-1):
            dataset_film[i,:] = Globals.profiles_film_dataset_ROI_red_channel_dose[int((i*15)+7),:]
        try:
            dataset_film[dataset_film.shape[0]-1,:] = Globals.profiles_film_dataset_ROI_red_channel_dose[int((dataset_film.shape[0]-1)*15+7), :]
        except:
            dataset_film[dataset_film.shape[0]-1,:] = \
                Globals.profiles_film_dataset_ROI_red_channel_dose[Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0]-1,:]


        line_doseplan = Globals.doseplan_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        line_film_dosemap = Globals.film_dose_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')
        line_film = Globals.film_write_image.create_line(0,Globals.doseplan_write_image_var_x,\
            Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x, fill='red')

        Globals.profiles_lines.append(line_doseplan)
        Globals.profiles_lines.append(line_film_dosemap)
        Globals.profiles_lines.append(line_film)

        def up_button_pressed(event):
            temp_x = Globals.doseplan_write_image_var_x - 15
            if(temp_x < 0):
                #Outside the frame
                return
            #inside the frame
            Globals.doseplan_write_image_var_x = temp_x
            Globals.profiles_coordinate_in_dataset = int(temp_x/15)
            Globals.doseplan_write_image.coords(line_doseplan,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_dose_write_image.coords(line_film_dosemap, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_write_image.coords(line_film, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        def down_button_pressed(event):
            temp_x = Globals.doseplan_write_image_var_x + 15
            if(temp_x >= Globals.doseplan_write_image_height):
                #Outside the frame
                return
            #Inside the frame
            Globals.profiles_coordinate_in_dataset = int(temp_x/15)
            Globals.doseplan_write_image_var_x = temp_x
            Globals.doseplan_write_image.coords(line_doseplan,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_dose_write_image.coords(line_film_dosemap,0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            Globals.film_write_image.coords(line_film, 0,Globals.doseplan_write_image_var_x,\
                Globals.doseplan_write_image_width,Globals.doseplan_write_image_var_x)
            draw('h', dataset_film,Globals.profiles_doseplan_dataset_ROI)

        Globals.form.bind("<Up>", up_button_pressed)
        Globals.form.bind("<Down>", down_button_pressed)

        if Globals.profiles_first_time_in_drawProfiles:
            Globals.profiles_first_time_in_drawProfiles = False
            draw('h', dataset_film, Globals.profiles_doseplan_dataset_ROI)

    elif(Globals.profiles_choice_of_profile_line_type.get() == 'v' and Globals.profiles_dataset_doseplan.PixelSpacing == [1, 1]):
        dataset_film = np.zeros(\
            (Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0], Globals.profiles_doseplan_dataset_ROI.shape[1]))
        for i in range(dataset_film.shape[1]-1):
            dataset_film[:,i] = Globals.profiles_film_dataset_ROI_red_channel_dose[:,int((i*5)+2)]
        try:
            dataset_film[:,dataset_film.shape[1]-1] = Globals.profiles_film_dataset_ROI_red_channel_dose[:,int((dataset_film.shape[1]-1)*5+2)]
        except:
            dataset_film[:,dataset_film.shape[1]-1] = \
                Globals.profiles_film_dataset_ROI_red_channel_dose[:,Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]-1]


        line_doseplan = Globals.doseplan_write_image.create_line(Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height, fill='red')
        line_film_dosemap = Globals.film_dose_write_image.create_line(Globals.doseplan_write_image_var_y,0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height, fill='red')
        line_film = Globals.film_write_image.create_line(Globals.doseplan_write_image_var_y,0,\
            Globals.doseplan_write_image_var_y,Globals.doseplan_write_image_height, fill='red')
        
        Globals.profiles_lines.append(line_doseplan)
        Globals.profiles_lines.append(line_film_dosemap)
        Globals.profiles_lines.append(line_film)
    
        def left_button_pressed(event):
            temp_y = Globals.doseplan_write_image_var_y - 5
            if(temp_y < 0):
                #Outside the frame
                return
            #inside the frame
            Globals.doseplan_write_image_var_y = temp_y
            Globals.profiles_coordinate_in_dataset = int(temp_y/5)
            Globals.doseplan_write_image.coords(line_doseplan,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_dose_write_image.coords(line_film_dosemap, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_write_image.coords(line_film, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        def right_button_pressed(event):
            temp_y = Globals.doseplan_write_image_var_y + 5
            if(temp_y >= Globals.doseplan_write_image_width):
                #Outside the frame
                return
            #Inside the frame
            Globals.profiles_coordinate_in_dataset = int(temp_y/5)
            Globals.doseplan_write_image_var_y = temp_y
            Globals.doseplan_write_image.coords(line_doseplan,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_dose_write_image.coords(line_film_dosemap,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_write_image.coords(line_film, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)
            

        Globals.form.bind("<Left>", left_button_pressed)
        Globals.form.bind("<Right>", right_button_pressed)

        if Globals.profiles_first_time_in_drawProfiles:
            Globals.profiles_first_time_in_drawProfiles = False
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)

    elif(Globals.profiles_choice_of_profile_line_type.get() == 'v' and Globals.profiles_dataset_doseplan.PixelSpacing == [2, 2]):
        dataset_film = np.zeros(\
            (Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0], Globals.profiles_doseplan_dataset_ROI.shape[1]))
        for i in range(dataset_film.shape[1]-1):
            dataset_film[:,i] = Globals.profiles_film_dataset_ROI_red_channel_dose[:,int((i*10)+5)]
        try:
            dataset_film[:,dataset_film.shape[1]-1] = Globals.profiles_film_dataset_ROI_red_channel_dose[:,int((dataset_film.shape[1]-1)*10+5)]
        except:
            dataset_film[:,dataset_film.shape[1]-1] = \
                Globals.profiles_film_dataset_ROI_red_channel_dose[:,Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]-1]


        line_doseplan = Globals.doseplan_write_image.create_line(Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height, fill='red')
        line_film_dosemap = Globals.film_dose_write_image.create_line(Globals.doseplan_write_image_var_y,0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height, fill='red')
        line_film = Globals.film_write_image.create_line(Globals.doseplan_write_image_var_y,0,\
            Globals.doseplan_write_image_var_y,Globals.doseplan_write_image_height, fill='red')
        
        Globals.profiles_lines.append(line_doseplan)
        Globals.profiles_lines.append(line_film_dosemap)
        Globals.profiles_lines.append(line_film)
    
        def left_button_pressed(event):
            temp_y = Globals.doseplan_write_image_var_y - 10
            if(temp_y < 0):
                #Outside the frame
                return
            #inside the frame
            Globals.doseplan_write_image_var_y = temp_y
            Globals.profiles_coordinate_in_dataset = int(temp_y/10)
            Globals.doseplan_write_image.coords(line_doseplan,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_dose_write_image.coords(line_film_dosemap, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_write_image.coords(line_film, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        def right_button_pressed(event):
            temp_y = Globals.doseplan_write_image_var_y + 10
            if(temp_y >= Globals.doseplan_write_image_width):
                #Outside the frame
                return
            #Inside the frame
            Globals.profiles_coordinate_in_dataset = int(temp_y/10)
            Globals.doseplan_write_image_var_y = temp_y
            Globals.doseplan_write_image.coords(line_doseplan,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_dose_write_image.coords(line_film_dosemap,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_write_image.coords(line_film, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)
            

        Globals.form.bind("<Left>", left_button_pressed)
        Globals.form.bind("<Right>", right_button_pressed)

        if Globals.profiles_first_time_in_drawProfiles:
            Globals.profiles_first_time_in_drawProfiles = False
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)

    elif(Globals.profiles_choice_of_profile_line_type.get() == 'v' and Globals.profiles_dataset_doseplan.PixelSpacing == [3, 3]):
        dataset_film = np.zeros(\
            (Globals.profiles_film_dataset_ROI_red_channel_dose.shape[0], Globals.profiles_doseplan_dataset_ROI.shape[1]))
        for i in range(dataset_film.shape[1]-1):
            dataset_film[:,i] = Globals.profiles_film_dataset_ROI_red_channel_dose[:,int((i*15)+7)]
        try:
            dataset_film[:,dataset_film.shape[1]-1] = Globals.profiles_film_dataset_ROI_red_channel_dose[:,int((dataset_film.shape[1]-1)*15+7)]
        except:
            dataset_film[:,dataset_film.shape[1]-1] = \
                Globals.profiles_film_dataset_ROI_red_channel_dose[:,Globals.profiles_film_dataset_ROI_red_channel_dose.shape[1]-1]


        line_doseplan = Globals.doseplan_write_image.create_line(Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height, fill='red')
        line_film_dosemap = Globals.film_dose_write_image.create_line(Globals.doseplan_write_image_var_y,0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height, fill='red')
        line_film = Globals.film_write_image.create_line(Globals.doseplan_write_image_var_y,0,\
            Globals.doseplan_write_image_var_y,Globals.doseplan_write_image_height, fill='red')
        
        Globals.profiles_lines.append(line_doseplan)
        Globals.profiles_lines.append(line_film_dosemap)
        Globals.profiles_lines.append(line_film)
    
        def left_button_pressed(event):
            temp_y = Globals.doseplan_write_image_var_y - 15
            if(temp_y < 0):
                #Outside the frame
                return
            #inside the frame
            Globals.doseplan_write_image_var_y = temp_y
            Globals.profiles_coordinate_in_dataset = int(temp_y/15)
            Globals.doseplan_write_image.coords(line_doseplan,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_dose_write_image.coords(line_film_dosemap, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_write_image.coords(line_film, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)

        def right_button_pressed(event):
            temp_y = Globals.doseplan_write_image_var_y + 15
            if(temp_y >= Globals.doseplan_write_image_width):
                #Outside the frame
                return
            #Inside the frame
            Globals.profiles_coordinate_in_dataset = int(temp_y/15)
            Globals.doseplan_write_image_var_y = temp_y
            Globals.doseplan_write_image.coords(line_doseplan,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_dose_write_image.coords(line_film_dosemap,Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            Globals.film_write_image.coords(line_film, Globals.doseplan_write_image_var_y, 0,\
            Globals.doseplan_write_image_var_y, Globals.doseplan_write_image_height)
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)
            

        Globals.form.bind("<Left>", left_button_pressed)
        Globals.form.bind("<Right>", right_button_pressed)

        if Globals.profiles_first_time_in_drawProfiles:
            Globals.profiles_first_time_in_drawProfiles = False
            draw('v', dataset_film, Globals.profiles_doseplan_dataset_ROI)
    elif(Globals.profiles_choice_of_profile_line_type.get() == 'd' and Globals.profiles_dataset_doseplan.PixelSpacing == [1, 1]):
        start_point = [0,0]
        def mousePushed(event):
            start_point = [event.x, event.y]
            if not len(Globals.profiles_lines)==0:
                Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
                Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
                Globals.film_write_image.delete(Globals.profiles_lines[2])
                Globals.profiles_lines = []

            line_doseplan = Globals.doseplan_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')
            line_film_dosemap = Globals.film_dose_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')
            line_film = Globals.film_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')

            Globals.profiles_lines.append(line_doseplan)
            Globals.profiles_lines.append(line_film_dosemap)
            Globals.profiles_lines.append(line_film)

            def mouseMoving(event):
                Globals.doseplan_write_image.coords(line_doseplan, start_point[0], start_point[1], event.x, event.y)
                Globals.film_dose_write_image.coords(line_film_dosemap, start_point[0], start_point[1], event.x, event.y)
                Globals.film_write_image.coords(line_film, start_point[0], start_point[1], event.x, event.y)

                

            Globals.film_dose_write_image.bind("<B1-Motion>", mouseMoving)

            def mouseReleased(event):
                Globals.end_point = [event.x, event.y]
                Globals.doseplan_write_image.coords(line_doseplan, start_point[0], start_point[1], event.x, event.y)
                Globals.film_dose_write_image.coords(line_film_dosemap, start_point[0], start_point[1], event.x, event.y)
                Globals.film_write_image.coords(line_film, start_point[0], start_point[1], event.x, event.y)
                Globals.profiles_line_coords_film = getCoordsInRandomLine(start_point[1], start_point[0], Globals.end_point[1], Globals.end_point[0])
                Globals.profiles_line_coords_doseplan = getCoordsInRandomLine(int(start_point[1]/5), int(start_point[0]/5), \
                    int(Globals.end_point[1]/5), int(Globals.end_point[0]/5))
                Globals.profiles_dataset_film_variable_draw = np.zeros(len(Globals.profiles_line_coords_film))
                Globals.profiles_dataset_doesplan_variable_draw=np.zeros(len(Globals.profiles_line_coords_doseplan))
                
                for i in range(len(Globals.profiles_dataset_film_variable_draw)):
                    coord = Globals.profiles_line_coords_film[i]
                    #print(coord[1], ", ", coord[0])
                    Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
                for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
                    Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]

                draw('d', Globals.profiles_dataset_film_variable_draw, Globals.profiles_dataset_doesplan_variable_draw)

            Globals.film_dose_write_image.bind("<ButtonRelease-1>", mouseReleased)
        Globals.film_dose_write_image.bind("<Button-1>", mousePushed)
       

    elif(Globals.profiles_choice_of_profile_line_type.get() == 'd' and Globals.profiles_dataset_doseplan.PixelSpacing == [2, 2]):
        start_point = [0,0]
        def mousePushed(event):
            start_point = [event.x, event.y]
            if not len(Globals.profiles_lines)==0:
                Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
                Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
                Globals.film_write_image.delete(Globals.profiles_lines[2])
                Globals.profiles_lines = []

            line_doseplan = Globals.doseplan_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')
            line_film_dosemap = Globals.film_dose_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')
            line_film = Globals.film_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')

            Globals.profiles_lines.append(line_doseplan)
            Globals.profiles_lines.append(line_film_dosemap)
            Globals.profiles_lines.append(line_film)

            def mouseMoving(event):
                Globals.doseplan_write_image.coords(line_doseplan, start_point[0], start_point[1], event.x, event.y)
                Globals.film_dose_write_image.coords(line_film_dosemap, start_point[0], start_point[1], event.x, event.y)
                Globals.film_write_image.coords(line_film, start_point[0], start_point[1], event.x, event.y)

                

            Globals.film_dose_write_image.bind("<B1-Motion>", mouseMoving)

            def mouseReleased(event):
                Globals.end_point = [event.x, event.y]
                Globals.doseplan_write_image.coords(line_doseplan, start_point[0], start_point[1], event.x, event.y)
                Globals.film_dose_write_image.coords(line_film_dosemap, start_point[0], start_point[1], event.x, event.y)
                Globals.film_write_image.coords(line_film, start_point[0], start_point[1], event.x, event.y)
                Globals.profiles_line_coords_film = getCoordsInRandomLine(start_point[1], start_point[0], Globals.end_point[1], Globals.end_point[0])
                Globals.profiles_line_coords_doseplan = getCoordsInRandomLine(int(start_point[1]/10), int(start_point[0]/10), \
                    int(Globals.end_point[1]/10), int(Globals.end_point[0]/10))
                Globals.profiles_dataset_film_variable_draw = np.zeros(len(Globals.profiles_line_coords_film))
                Globals.profiles_dataset_doesplan_variable_draw=np.zeros(len(Globals.profiles_line_coords_doseplan))
                
                for i in range(len(Globals.profiles_dataset_film_variable_draw)):
                    coord = Globals.profiles_line_coords_film[i]
                    #print(coord[1], ", ", coord[0])
                    Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
                for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
                    Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]

                draw('d', Globals.profiles_dataset_film_variable_draw, Globals.profiles_dataset_doesplan_variable_draw)

            Globals.film_dose_write_image.bind("<ButtonRelease-1>", mouseReleased)
        Globals.film_dose_write_image.bind("<Button-1>", mousePushed)
    elif(Globals.profiles_choice_of_profile_line_type.get() == 'd' and Globals.profiles_dataset_doseplan.PixelSpacing == [3, 3]):
        start_point = [0,0]
        def mousePushed(event):
            start_point = [event.x, event.y]
            if not len(Globals.profiles_lines)==0:
                Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
                Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
                Globals.film_write_image.delete(Globals.profiles_lines[2])
                Globals.profiles_lines = []

            line_doseplan = Globals.doseplan_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')
            line_film_dosemap = Globals.film_dose_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')
            line_film = Globals.film_write_image.create_line(start_point[0], start_point[1],start_point[0],start_point[1], fill='red')

            Globals.profiles_lines.append(line_doseplan)
            Globals.profiles_lines.append(line_film_dosemap)
            Globals.profiles_lines.append(line_film)

            def mouseMoving(event):
                Globals.doseplan_write_image.coords(line_doseplan, start_point[0], start_point[1], event.x, event.y)
                Globals.film_dose_write_image.coords(line_film_dosemap, start_point[0], start_point[1], event.x, event.y)
                Globals.film_write_image.coords(line_film, start_point[0], start_point[1], event.x, event.y)

                

            Globals.film_dose_write_image.bind("<B1-Motion>", mouseMoving)

            def mouseReleased(event):
                Globals.end_point = [event.x, event.y]
                Globals.doseplan_write_image.coords(line_doseplan, start_point[0], start_point[1], event.x, event.y)
                Globals.film_dose_write_image.coords(line_film_dosemap, start_point[0], start_point[1], event.x, event.y)
                Globals.film_write_image.coords(line_film, start_point[0], start_point[1], event.x, event.y)
                Globals.profiles_line_coords_film = getCoordsInRandomLine(start_point[1], start_point[0], Globals.end_point[1], Globals.end_point[0])
                Globals.profiles_line_coords_doseplan = getCoordsInRandomLine(int(start_point[1]/15), int(start_point[0]/15), \
                    int(Globals.end_point[1]/15), int(Globals.end_point[0]/15))
                Globals.profiles_dataset_film_variable_draw = np.zeros(len(Globals.profiles_line_coords_film))
                Globals.profiles_dataset_doesplan_variable_draw=np.zeros(len(Globals.profiles_line_coords_doseplan))
                
                for i in range(len(Globals.profiles_dataset_film_variable_draw)):
                    coord = Globals.profiles_line_coords_film[i]
                    #print(coord[1], ", ", coord[0])
                    Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
                for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
                    Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]

                draw('d', Globals.profiles_dataset_film_variable_draw, Globals.profiles_dataset_doesplan_variable_draw)

            Globals.film_dose_write_image.bind("<ButtonRelease-1>", mouseReleased)
        Globals.film_dose_write_image.bind("<Button-1>", mousePushed)
    else:
        messagebox.showerror("Error", "Fatal error. Something went wrong, try again \n(Code: drawProfiles)")
        return
        
def trace_profileLineType(var, indx, mode):
    test_drawProfiles()


def test_drawProfiles():
    if Globals.profiles_dataset_doseplan == None:
        return
    else:
        Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
        Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
        Globals.film_write_image.delete(Globals.profiles_lines[2])
        Globals.form.unbind("<Up>")
        Globals.form.unbind("<Down>")
        Globals.form.unbind("<Left>")
        Globals.form.unbind("<Rigth>")
        Globals.profiles_first_time_in_drawProfiles = True
        drawProfiles(False)


def adjustROILeft(line_orient):
    if not line_orient == 'd':
        Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
        Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
        Globals.film_write_image.delete(Globals.profiles_lines[2])
    if(Globals.profiles_film_variable_ROI_coords[2]-1 < 0):
        messagebox.showwarning("Warning", "Reached end of film \n(Code: adjustROILeft)")
        return
    Globals.profiles_film_variable_ROI_coords = \
        [Globals.profiles_film_variable_ROI_coords[0], Globals.profiles_film_variable_ROI_coords[1],\
            Globals.profiles_film_variable_ROI_coords[2]-1, Globals.profiles_film_variable_ROI_coords[3]-1]
    Globals.profiles_film_dataset_ROI_red_channel_dose = \
        Globals.profiles_film_dataset_red_channel_dose\
            [Globals.profiles_film_variable_ROI_coords[0]:Globals.profiles_film_variable_ROI_coords[1],\
                Globals.profiles_film_variable_ROI_coords[2]:Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_first_time_in_drawProfiles = True
    if line_orient == 'd':
        for i in range(len(Globals.profiles_dataset_film_variable_draw)):
            coord = Globals.profiles_line_coords_film[i]
            #print(coord[1], ", ", coord[0])
            Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
        for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
            Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]
        drawProfiles(True)
    else:
        drawProfiles(False)

def adjustROIRight(line_orient):
    if not line_orient == 'd':
        Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
        Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
        Globals.film_write_image.delete(Globals.profiles_lines[2])
    if(Globals.profiles_film_variable_ROI_coords[3]+1 > Globals.profiles_film_dataset_red_channel_dose.shape[1]):
        messagebox.showwarning("Warning", "Reached end of film \n(Code: adjustROIRight)")
        return
    Globals.profiles_film_variable_ROI_coords = \
        [Globals.profiles_film_variable_ROI_coords[0], Globals.profiles_film_variable_ROI_coords[1],\
            Globals.profiles_film_variable_ROI_coords[2]+1, Globals.profiles_film_variable_ROI_coords[3]+1]
    Globals.profiles_film_dataset_ROI_red_channel_dose = \
        Globals.profiles_film_dataset_red_channel_dose\
            [Globals.profiles_film_variable_ROI_coords[0]:Globals.profiles_film_variable_ROI_coords[1],\
                Globals.profiles_film_variable_ROI_coords[2]:Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_first_time_in_drawProfiles = True
    if line_orient == 'd':
        for i in range(len(Globals.profiles_dataset_film_variable_draw)):
            coord = Globals.profiles_line_coords_film[i]
            #print(coord[1], ", ", coord[0])
            Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
        for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
            Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]
        drawProfiles(True)
    else:
        drawProfiles(False)

def adjustROIUp(line_orient):
    if not line_orient == 'd':
        Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
        Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
        Globals.film_write_image.delete(Globals.profiles_lines[2])
    if(Globals.profiles_film_variable_ROI_coords[0]-1 < 0):
        messagebox.showwarning("Warning", "Reached end of film \n(Code: adjustROIUp)")
        return
    Globals.profiles_film_variable_ROI_coords = \
        [Globals.profiles_film_variable_ROI_coords[0]-1, Globals.profiles_film_variable_ROI_coords[1]-1,\
            Globals.profiles_film_variable_ROI_coords[2], Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_film_dataset_ROI_red_channel_dose = \
        Globals.profiles_film_dataset_red_channel_dose\
            [Globals.profiles_film_variable_ROI_coords[0]:Globals.profiles_film_variable_ROI_coords[1],\
                Globals.profiles_film_variable_ROI_coords[2]:Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_first_time_in_drawProfiles = True
    if line_orient == 'd':
        for i in range(len(Globals.profiles_dataset_film_variable_draw)):
            coord = Globals.profiles_line_coords_film[i]
            #print(coord[1], ", ", coord[0])
            Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
        for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
            Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]
        drawProfiles(True)
    else:
        drawProfiles(False)

def adjustROIDown(line_orient):
    if not line_orient == 'd':
        Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
        Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
        Globals.film_write_image.delete(Globals.profiles_lines[2])
    if(Globals.profiles_film_variable_ROI_coords[1]+1 > Globals.profiles_film_dataset_red_channel_dose.shape[0]):
        messagebox.showwarning("Warning", "Reached end of film \n(Code: adjustROIDown)")
        return
    Globals.profiles_film_variable_ROI_coords = \
        [Globals.profiles_film_variable_ROI_coords[0]+1, Globals.profiles_film_variable_ROI_coords[1]+1,\
            Globals.profiles_film_variable_ROI_coords[2], Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_film_dataset_ROI_red_channel_dose = \
        Globals.profiles_film_dataset_red_channel_dose\
            [Globals.profiles_film_variable_ROI_coords[0]:Globals.profiles_film_variable_ROI_coords[1],\
                Globals.profiles_film_variable_ROI_coords[2]:Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_first_time_in_drawProfiles = True
    if line_orient == 'd':
        for i in range(len(Globals.profiles_dataset_film_variable_draw)):
            coord = Globals.profiles_line_coords_film[i]
            #print(coord[1], ", ", coord[0])
            Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
        for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
            Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]
        drawProfiles(True)
    else:
        drawProfiles(False)

def returnToOriginalROICoordinates(line_orient):
    if not line_orient == 'd':
        Globals.doseplan_write_image.delete(Globals.profiles_lines[0])
        Globals.film_dose_write_image.delete(Globals.profiles_lines[1])
        Globals.film_write_image.delete(Globals.profiles_lines[2])
    Globals.profiles_film_variable_ROI_coords = \
        [Globals.profiles_ROI_coords[0][1], Globals.profiles_ROI_coords[2][1],\
                Globals.profiles_ROI_coords[0][0], Globals.profiles_ROI_coords[1][0]]
    
    Globals.profiles_film_dataset_ROI_red_channel_dose = \
        Globals.profiles_film_dataset_red_channel_dose\
            [Globals.profiles_film_variable_ROI_coords[0]:Globals.profiles_film_variable_ROI_coords[1],\
                Globals.profiles_film_variable_ROI_coords[2]:Globals.profiles_film_variable_ROI_coords[3]]
    Globals.profiles_first_time_in_drawProfiles = True
    if line_orient == 'd':
        for i in range(len(Globals.profiles_dataset_film_variable_draw)):
            coord = Globals.profiles_line_coords_film[i]
            #print(coord[1], ", ", coord[0])
            Globals.profiles_dataset_film_variable_draw[i] = Globals.profiles_film_dataset_ROI_red_channel_dose[coord[0], coord[1]]
                
        for i in range(len(Globals.profiles_dataset_doesplan_variable_draw)):
            Globals.profiles_dataset_doesplan_variable_draw[i] = Globals.profiles_doseplan_dataset_ROI[int(Globals.profiles_line_coords_doseplan[i][0]), int(Globals.profiles_line_coords_doseplan[i][1])]
        drawProfiles(True)
    else:
        drawProfiles(False)

def pixel_to_dose(P,a,b,c):
    ret = c + b/(P-a)
    return ret

def processDoseplan_usingReferencePoint(only_one):

    ################  RT Plan ######################

    #Find each coordinate in mm to isocenter relative to first element in doseplan
    iso_1 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[0] - Globals.profiles_isocenter_mm[0])
    iso_2 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[1] - Globals.profiles_isocenter_mm[1])
    iso_3 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[2] - Globals.profiles_isocenter_mm[2])
    #Given as [x,y,z] in patient coordinates
    Globals.profiles_isocenter_mm = [iso_1, iso_2, iso_3]
    
    #Reads input displacement from phantom on reference point in film
    #lateral = Globals.profiles_input_lateral_displacement.get("1.0",'end-1c')
    #vertical = Globals.profiles_input_vertical_displacement.get("1.0", 'end-1c')
    #longit = Globals.profiles_input_longitudinal_displacement.get("1.0", 'end-1c')
    #if(lateral==" "):lateral=0
    #if(vertical==" "):vertical=0
    #if(longit==" "):longit=0
    try:
        Globals.profiles_vertical = int(Globals.profiles_vertical)
    except:
        messagebox.showerror("Error", "Could not read the vertical displacements\n (Code: displacements to integer)")
        return
    try:
        Globals.profiles_lateral = int(Globals.profiles_lateral)
    except:
        messagebox.showerror("Error", "Could not read the lateral displacements\n (Code: displacements to integer)")
        return
    try:
        Globals.profiles_longitudinal = int(Globals.profiles_longitudinal)
    except:
        messagebox.showerror("Error", "Could not read the longitudinal displacements\n (Code: displacements to integer)")
        return

    lateral = Globals.profiles_lateral
    longit = Globals.profiles_longitudinal
    vertical = Globals.profiles_vertical
    isocenter_px = np.zeros(3)
    distance_in_doseplan_ROI_reference_point_px = []
    if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
        #make isocenter coordinates into pixel values
        isocenter_px[0] = np.round(iso_1)
        isocenter_px[1] = np.round(iso_2)
        isocenter_px[2] = np.round(iso_3)

        #find the pixel distance from reference point to ROI corners
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_reference_point_ROI[0][0]),\
            np.round(Globals.profiles_distance_reference_point_ROI[0][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_reference_point_ROI[1][0]),\
            np.round(Globals.profiles_distance_reference_point_ROI[1][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_reference_point_ROI[2][0]),\
            np.round(Globals.profiles_distance_reference_point_ROI[2][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_reference_point_ROI[3][0]),\
            np.round(Globals.profiles_distance_reference_point_ROI[3][1])])

        #Input to px
        lateral_px = np.round(lateral)
        vertical_px = np.round(vertical)
        longit_px = np.round(longit)

        #displacment to px
        doseplan_lateral_displacement_px = np.round(Globals.profiles_doseplan_lateral_displacement)
        doseplan_vertical_displacement_px = np.round(Globals.profiles_doseplan_vertical_displacement)
        doseplan_longitudinal_displacement_px = np.round(Globals.profiles_doseplan_longitudianl_displacement)

    elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
        #make isocenter coordinates into pixel values
        isocenter_px[0] = np.round(iso_1/2)
        isocenter_px[1] = np.round(iso_2/2)
        isocenter_px[2] = np.round(iso_3/2)

        #find the pixel distance from reference point to ROI corners
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[0][0])/2),\
            np.round((Globals.profiles_distance_reference_point_ROI[0][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[1][0])/2),\
            np.round((Globals.profiles_distance_reference_point_ROI[1][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[2][0])/2),\
            np.round((Globals.profiles_distance_reference_point_ROI[2][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[3][0])/2),\
            np.round((Globals.profiles_distance_reference_point_ROI[3][1])/2)])

        #Input to px
        lateral_px = np.round(lateral/2)
        vertical_px = np.round(vertical/2)
        longit_px = np.round(longit/2)

        #displacment to pc
        doseplan_lateral_displacement_px = np.round((Globals.profiles_doseplan_lateral_displacement)/2)
        doseplan_vertical_displacement_px = np.round((Globals.profiles_doseplan_vertical_displacement)/2)
        doseplan_longitudinal_displacement_px = np.round((Globals.profiles_doseplan_longitudianl_displacement)/2)

    else:
        #make isocenter coordinates into pixel values
        isocenter_px[0] = np.round(iso_1/3)
        isocenter_px[1] = np.round(iso_2/3)
        isocenter_px[2] = np.round(iso_3/3)

        #find the pixel distance from reference point to ROI corners
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[0][0])/3),\
            np.round((Globals.profiles_distance_reference_point_ROI[0][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[1][0])/3),\
            np.round((Globals.profiles_distance_reference_point_ROI[1][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[2][0])/3),\
            np.round((Globals.profiles_distance_reference_point_ROI[2][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_reference_point_ROI[3][0])/3),\
            np.round((Globals.profiles_distance_reference_point_ROI[3][1])/3)])

        #Input to px
        lateral_px = np.round(lateral/3)
        vertical_px = np.round(vertical/3)
        longit_px = np.round(longit/3)

        #displacment to pc
        doseplan_lateral_displacement_px = np.round((Globals.profiles_doseplan_lateral_displacement)/3)
        doseplan_vertical_displacement_px = np.round((Globals.profiles_doseplan_vertical_displacement)/3)
        doseplan_longitudinal_displacement_px = np.round((Globals.profiles_doseplan_longitudianl_displacement)/3)

    temp_ref_point_doseplan = np.zeros(3)

    #Finding reference point in doseplan
    if(Globals.profiles_doseplan_patient_position=='HFS'):
        temp_ref_point_doseplan[0] = int(isocenter_px[0]+ doseplan_lateral_displacement_px - lateral_px)
        temp_ref_point_doseplan[1] = int(isocenter_px[1]- doseplan_vertical_displacement_px + vertical_px)
        temp_ref_point_doseplan[2] = int(isocenter_px[2]+ doseplan_longitudinal_displacement_px - longit_px)
    elif(Globals.profiles_doseplan_patient_position=='HFP'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- doseplan_lateral_displacement_px+ lateral_px
        temp_ref_point_doseplan[1] = isocenter_px[1]+ doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[2] = isocenter_px[2]+ doseplan_longitudinal_displacement_px - longit_px
    elif(Globals.profiles_doseplan_patient_position=='HFDR'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- doseplan_vertical_displacement_px + vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1]+ doseplan_lateral_displacement_px - lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]+ doseplan_longitudinal_displacement_px - longit_px
    elif(Globals.profiles_doseplan_patient_position=='HFDL'):
        temp_ref_point_doseplan[0] = isocenter_px[0]+ doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1]- doseplan_lateral_displacement_px + lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]+ doseplan_longitudinal_displacement_px - longit_px
    elif(Globals.profiles_doseplan_patient_position=='FFS'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- doseplan_lateral_displacement_px + lateral_px
        temp_ref_point_doseplan[1] = isocenter_px[1]+ doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- doseplan_longitudinal_displacement_px + longit_px
    elif(Globals.profiles_doseplan_patient_position=='FFP'):
        temp_ref_point_doseplan[0] = isocenter_px[0]+ doseplan_lateral_displacement_px- lateral_px
        temp_ref_point_doseplan[1] = isocenter_px[1]- doseplan_vertical_displacement_px + vertical_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- doseplan_longitudinal_displacement_px + longit_px
    elif(Globals.profiles_doseplan_patient_position=='FFDR'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- doseplan_vertical_displacement_px + vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1]- doseplan_lateral_displacement_px + lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- doseplan_longitudinal_displacement_px + longit_px
    else:
        temp_ref_point_doseplan[0] = isocenter_px[0] + doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1] + doseplan_lateral_displacement_px - lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- doseplan_longitudinal_displacement_px + longit_px

    Globals.profiles_reference_point_in_doseplan = temp_ref_point_doseplan
    reference_point = np.zeros(3)

    ######################## Doseplan ##################################
    #dataset_swapped is now the dataset entered the same way as expected with film (slice, rows, columns)
    #isocenter_px and reference_point is not turned according to the doseplan and film orientation.
    if(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 1, 0]):
        reference_point[0] = temp_ref_point_doseplan[2]
        reference_point[1] = temp_ref_point_doseplan[1]
        reference_point[2] = temp_ref_point_doseplan[0]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #number of frames -> rows
            #rows -> number of frames
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #column -> number of frames
            #number of frames -> rows
            #rows -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            #dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            #temp_ref = reference_point[0]
            #reference_point[0] = reference_point[1]
            #reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        else:
            messagebox.showerror("Error", "Something has gone wrong here.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 0, 1]):
        reference_point[0] = temp_ref_point_doseplan[1]
        reference_point[1] = temp_ref_point_doseplan[2]
        reference_point[2] = temp_ref_point_doseplan[0]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 1, 0, 0]):
        reference_point[0] = temp_ref_point_doseplan[2]
        reference_point[1] = temp_ref_point_doseplan[0]
        reference_point[2] = temp_ref_point_doseplan[1]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 0, 0, 1]):
        reference_point[0] = temp_ref_point_doseplan[0]
        reference_point[1] = temp_ref_point_doseplan[2]
        reference_point[2] = temp_ref_point_doseplan[1]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 1, 0, 0]):
        reference_point[0] = temp_ref_point_doseplan[1]
        reference_point[1] = temp_ref_point_doseplan[0]
        reference_point[2] = temp_ref_point_doseplan[2]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 0, 1, 0]):
        reference_point[0] = temp_ref_point_doseplan[0]
        reference_point[1] = temp_ref_point_doseplan[1]
        reference_point[2] = temp_ref_point_doseplan[2]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
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
    
    if(reference_point[0]<0 or reference_point[0]>dataset_swapped.shape[0]):
        messagebox.showerror("Error", "Reference point is outside of dosematrix\n\
            (Code: first dimension, number of frames in dosematrix)")
        return
    if(reference_point[1]<0 or reference_point[1]>dataset_swapped.shape[1]):
        messagebox.showerror("Error", "Reference point is outside of dosematrix\n\
            (Code: second dimension, rows in dosematrix)")
        return
    if(reference_point[2]<0 or reference_point[2]>dataset_swapped.shape[2]):
        messagebox.showerror("Error", "Reference point is outside of dosematrix\n\
            (Code: third dimension, columns in dosematrix)")
        return

    dose_slice = dataset_swapped[int(reference_point[0]),:,:]
    
    
 
    #calculate the coordinates of the Region of Interest in doseplan (marked on the film) 
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

    if only_one:
        Globals.profiles_doseplan_dataset_ROI = \
            dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
   
        img=Globals.profiles_doseplan_dataset_ROI
        if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
            img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
        elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
            img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
        else:
            img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        mx=np.max(img)
        Globals.max_dose_doseplan = mx*Globals.profiles_dose_scaling_doseplan
        img = img/mx
        PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img)*255))

        wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
        doseplan_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
        doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
        Globals.profiles_film_panedwindow.add(doseplan_canvas, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())
        doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())


        Globals.doseplan_write_image = tk.Canvas(doseplan_canvas)
        Globals.doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
        Globals.doseplan_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

        doseplan_text_image_canvas = tk.Canvas(doseplan_canvas)
        doseplan_text_image_canvas.grid(row=0,column=0,sticky=N+S+W+E)
        doseplan_text_image_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            width=Globals.profiles_doseplan_text_image.width(), height=Globals.profiles_doseplan_text_image.height())

        scaled_image_visual = PIL_img_doseplan_ROI
        scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
        Globals.doseplan_write_image_width = scaled_image_visual.width()
        Globals.doseplan_write_image_height = scaled_image_visual.height()
        Globals.doseplan_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
        Globals.doseplan_write_image.image = scaled_image_visual
        doseplan_text_image_canvas.create_image(0,0,image=Globals.profiles_doseplan_text_image, anchor="nw")
        doseplan_text_image_canvas.image=Globals.profiles_doseplan_text_image

        drawProfiles(False)
    
    else:
        img=dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
        """
        if(Globals.profiles_number_of_doseplans == 1):
            Globals.profiles_doseplan_dataset_ROI_several = img
            Globals.profiles_number_of_doseplans+=1

            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
            else:
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        else:
            Globals.profiles_doseplan_dataset_ROI_several += img
            Globals.profiles_number_of_doseplans+=1
            
            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
            else:
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))
        """
        Globals.profiles_doseplan_dataset_ROI_several.append(img)
        Globals.profiles_number_of_doseplans+=1

        if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5)))
        elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10)))
        else:
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15)))


def processDoseplan_usingIsocenter(only_one):

    ################  RT Plan ######################

    #Find each coordinate in mm to isocenter relative to first element in doseplan
    iso_1 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[0] - Globals.profiles_isocenter_mm[0])
    iso_2 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[1] - Globals.profiles_isocenter_mm[1])
    iso_3 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[2] - Globals.profiles_isocenter_mm[2])
    #Given as [x,y,z] in patient coordinates
    Globals.profiles_isocenter_mm = [iso_1, iso_2, iso_3]


    #Isocenter in pixel relative to the first element in the doseplan
    isocenter_px = np.zeros(3)
    distance_in_doseplan_ROI_reference_point_px = []
    if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
        isocenter_px[0] = np.round(iso_1)#np.round(Globals.profiles_isocenter_mm[0])
        isocenter_px[1] = np.round(iso_2)#np.round(Globals.profiles_isocenter_mm[1])
        isocenter_px[2] = np.round(iso_3)#np.round(Globals.profiles_isocenter_mm[2])
        
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
        isocenter_px[0] = np.round(iso_1/2)#np.round(Globals.profiles_isocenter_mm[0]/2)
        isocenter_px[1] = np.round(iso_2/2)#np.round(Globals.profiles_isocenter_mm[1]/2)
        isocenter_px[2] = np.round(iso_3/2)#np.round(Globals.profiles_isocenter_mm[2]/2)
       
        
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
        isocenter_px[0] = np.round(iso_1/3)#np.round(Globals.profiles_isocenter_mm[0]/3)
        isocenter_px[1] = np.round(iso_2/3)#np.round(Globals.profiles_isocenter_mm[1]/3)
        isocenter_px[2] = np.round(iso_3/3)#np.round(Globals.profiles_isocenter_mm[2]/3)
        
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
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[2]
        reference_point[1] = isocenter_px[1]
        reference_point[2] = isocenter_px[0]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #number of frames -> rows
            #rows -> number of frames
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #column -> number of frames
            #number of frames -> rows
            #rows -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            #dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            #temp_ref = reference_point[0]
            #reference_point[0] = reference_point[1]
            #reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        else:
            messagebox.showerror("Error", "Something has gone wrong here.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 0, 1]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[1]
        reference_point[1] = isocenter_px[2]
        reference_point[2] = isocenter_px[0]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #columns -> number of frames
            #number of frames -> columns
            #rows -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> number of frames
            #number of frames -> rows
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 1, 0, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[2]
        reference_point[1] = isocenter_px[0]
        reference_point[2] = isocenter_px[1]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> columns
            #columns -> number of frames
            #number of frames -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #number -> rows
            #colums -> colums
            #rows -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #column -> rows
            #rows -> column
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 0, 0, 1]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[0]
        reference_point[1] = isocenter_px[2]
        reference_point[2] = isocenter_px[1]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> rows
            #columns -> number of frames
            #number of frames ->columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #number of frames -> columns
            #columns -> rows
            #rows -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 1, 0, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[1]
        reference_point[1] = isocenter_px[0]
        reference_point[2] = isocenter_px[2]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> columns
            #columns -> rows
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #rows -> number of frames
            #columns -> rows
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            #dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            #temp_ref = reference_point[1]
            #reference_point[1] = reference_point[2]
            #reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> columns
            #colums -> number of frames
            #number of frames -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 0, 1, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[0]
        reference_point[1] = isocenter_px[1]
        reference_point[2] = isocenter_px[2]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> number of frames
            #columns ->rows
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #rows -> columns
            #columns -> rows
            #number of frames -> number of frames
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
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
    
    if Globals.profiles_dataset_doseplan.PixelSpacing == [1, 1]:
        offset = int(np.round(Globals.profiles_offset))
        dose_slice = dataset_swapped[int(reference_point[0]) + offset]
    elif Globals.profiles_dataset_doseplan.PixelSpacing == [2, 2]:
        offset = int(np.round(Globals.profiles_offset/2))
        dose_slice = dataset_swapped[int(reference_point[0] + offset)]
    else:
        offset = int(np.round(Globals.profiles_offset/3))
        dose_slice = dataset_swapped[int(reference_point[0]) + offset]

        
    
    #calculate the coordinates of the Region of Interest in doseplan (marked on the film) 
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

    #dose_slice = cv2.flip(dose_slice, 1)
    if(only_one):
        Globals.profiles_doseplan_dataset_ROI = \
            dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
    
    
        img=Globals.profiles_doseplan_dataset_ROI
        if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
            img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
        elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
            img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
        else:
            img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        mx=np.max(img)
        Globals.max_dose_doseplan = mx*Globals.profiles_dose_scaling_doseplan
        max_dose = mx*Globals.profiles_dose_scaling_doseplan
        img = img/mx
        PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img)*255))

        wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
        doseplan_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
        doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
        Globals.profiles_film_panedwindow.add(doseplan_canvas, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())
        doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())


        Globals.doseplan_write_image = tk.Canvas(doseplan_canvas)
        Globals.doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
        Globals.doseplan_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

        doseplan_text_image_canvas = tk.Canvas(doseplan_canvas)
        doseplan_text_image_canvas.grid(row=0,column=0,sticky=N+S+W+E)
        doseplan_text_image_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            width=Globals.profiles_doseplan_text_image.width(), height=Globals.profiles_doseplan_text_image.height())

        scaled_image_visual = PIL_img_doseplan_ROI
        scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
        Globals.doseplan_write_image_width = scaled_image_visual.width()
        Globals.doseplan_write_image_height = scaled_image_visual.height()
        Globals.doseplan_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
        Globals.doseplan_write_image.image = scaled_image_visual
        doseplan_text_image_canvas.create_image(0,0,image=Globals.profiles_doseplan_text_image, anchor="nw")
        doseplan_text_image_canvas.image=Globals.profiles_doseplan_text_image

        drawProfiles(False)

    else:
        img=dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
        """
        if(Globals.profiles_number_of_doseplans == 1):
            Globals.profiles_doseplan_dataset_ROI_several = img
            Globals.profiles_number_of_doseplans+=1

            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
            else:
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        else:
            Globals.profiles_doseplan_dataset_ROI_several += img
            Globals.profiles_number_of_doseplans+=1
            
            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
            else:
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))
        """
        Globals.profiles_doseplan_dataset_ROI_several.append(img)
        Globals.profiles_number_of_doseplans+=1

        if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5)))
        elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10)))
        else:
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15)))

        
        



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
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file.\n\
            (Code: isocenter reading)")
        return

    try:
        Globals.profiles_doseplan_vertical_displacement = dataset.PatientSetupSequence[0].TableTopVerticalSetupDisplacement
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file. \n\
            (Code: vertical table displacement)")

    try:
        Globals.profiles_doseplan_lateral_displacement = dataset.PatientSetupSequence[0].TableTopLateralSetupDisplacement
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file-\n\
            (Code: lateral table displacement)")

    try:
        Globals.profiles_doseplan_longitudianl_displacement = dataset.PatientSetupSequence[0].TableTopLongitudinalSetupDisplacement
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file\n\
            (Code: longitudinal table displacement)")

    try:
        patient_position = dataset.PatientSetupSequence[0].PatientPosition
        Globals.profiles_doseplan_patient_position = patient_position
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. Try again or try another file\n\
            (Code: Patient position)")
    
    if(not(patient_position=='HFS' or patient_position=='HFP' or patient_position=='HFDR' or patient_position == 'HFDL'\
        or patient_position=='FFDR' or patient_position=='FFDL' or patient_position=='FFP' or patient_position=='FFS')):
        messagebox.showerror("Error", "Fidora does only support patient positions: \n\
            HFS, HFP, HFDR, HFDL, FFP, FFS, FFDR, FFDL")
        return
    
    Globals.profiles_test_if_added_rtplan = True
    #if(Globals.profiles_test_if_added_doseplan):
    #    if(Globals.profiles_isocenter_or_reference_point == "Isocenter"):
    #        processDoseplan_usingIsocenter(only_one)
    #    elif(Globals.profiles_isocenter_or_reference_point == "Ref_point"):
    #        processDoseplan_usingReferencePoint(only_one)
    #    else:
    #        messagebox.showerror("Error", "Something went wrong. Try again.\n\
    #            (Code: processDoseplan)")
    #        return
    Globals.profiles_upload_button_doseplan.config(state=ACTIVE)
    Globals.profiles_upload_button_rtplan.config(state=DISABLED)

def UploadDoseplan_button_function():
    yes = messagebox.askyesno("Question", "Are you going to upload several doseplans and/or use a factor on a plan?")
    if not yes:
        UploadDoseplan(True)
        return
    
    several_doseplans_window = tk.Toplevel(Globals.tab4_canvas)
    several_doseplans_window.geometry("600x500+10+10")
    several_doseplans_window.grab_set()
    
    doseplans_over_all_frame = tk.Frame(several_doseplans_window, bd=0, relief=FLAT)
    doseplans_over_all_canvas = Canvas(doseplans_over_all_frame)

    doseplans_xscrollbar = Scrollbar(doseplans_over_all_frame, orient=HORIZONTAL, command=doseplans_over_all_canvas.xview)
    doseplans_yscrollbar = Scrollbar(doseplans_over_all_frame, command=doseplans_over_all_canvas.yview)

    Globals.doseplans_scroll_frame = ttk.Frame(doseplans_over_all_canvas)
    Globals.doseplans_scroll_frame.bind("<Configure>", lambda e: doseplans_over_all_canvas.configure(scrollregion=doseplans_over_all_canvas.bbox('all')))

    doseplans_over_all_canvas.create_window((0,0), window=Globals.doseplans_scroll_frame, anchor='nw')
    doseplans_over_all_canvas.configure(xscrollcommand=doseplans_xscrollbar.set, yscrollcommand=doseplans_yscrollbar.set)

    doseplans_over_all_frame.config(highlightthickness=0, bg='#ffffff')
    doseplans_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
    doseplans_over_all_frame.pack(expand=True, fill=BOTH)
    doseplans_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
    doseplans_over_all_frame.grid_columnconfigure(0, weight=1)
    doseplans_over_all_frame.grid_rowconfigure(0, weight=1)
    doseplans_xscrollbar.grid(row=1, column=0, sticky=E+W)
    doseplans_over_all_frame.grid_columnconfigure(1, weight=0)
    doseplans_over_all_frame.grid_rowconfigure(1, weight=0)
    doseplans_yscrollbar.grid(row=0, column=1, sticky=N+S)
    doseplans_over_all_frame.grid_columnconfigure(2, weight=0)
    doseplans_over_all_frame.grid_rowconfigure(2, weight=0)

    upload_doseplan_frame = tk.Frame(Globals.doseplans_scroll_frame)
    upload_doseplan_frame.grid(row=0, column = 0, padx = (30,30), pady=(30,0), sticky=N+S+E+W)
    Globals.doseplans_scroll_frame.grid_columnconfigure(0, weight=0)
    Globals.doseplans_scroll_frame.grid_rowconfigure(0, weight=0)
    upload_doseplan_frame.config(bg = '#ffffff')

    upload_button_doseplan = tk.Button(upload_doseplan_frame, text='Browse', image=Globals.profiles_add_doseplans_button_image,\
        cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: UploadDoseplan(False))
    upload_button_doseplan.pack(expand=True, fill=BOTH)
    upload_button_doseplan.configure(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
    upload_button_doseplan.image = Globals.profiles_add_doseplans_button_image

    def closeUploadDoseplans():
        if(len(Globals.profiles_doseplan_dataset_ROI_several) == 0):
            messagebox.showinfo("INFO", "No doseplan has been uploaded")
            return
        for i in range(len(Globals.profiles_doseplan_dataset_ROI_several)):
            if Globals.profiles_doseplans_factor_input[i].get("1.0", 'end-1c') == " ":
                factor = 1
            else:
                try:
                    factor = float(Globals.profiles_doseplans_factor_input[i].get("1.0", 'end-1c'))
                except:
                    messagebox.showerror("Error", "Invalid factor. Must be number.\n (Code: closeUploadDoseplans)")
                    return
            if i == 0:
                doseplan_ROI = Globals.profiles_doseplan_dataset_ROI_several[i]
                doseplan_ROI= doseplan_ROI*factor

                img_ROI = Globals.profiles_several_img[i]
                img_ROI = img_ROI*factor
            else:
                doseplan_ROI+= factor*Globals.profiles_doseplan_dataset_ROI_several[i]
                img_ROI+= factor*Globals.profiles_several_img[i]

        

        mx=np.max(img_ROI)
        #max_dose = mx*Globals.profiles_dose_scaling_doseplan
        img_ROI = img_ROI/mx
        PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img_ROI)*255))

        wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
        doseplan_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
        doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
        Globals.profiles_film_panedwindow.add(doseplan_canvas, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())
        doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())


        Globals.doseplan_write_image = tk.Canvas(doseplan_canvas)
        Globals.doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
        Globals.doseplan_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

        doseplan_text_image_canvas = tk.Canvas(doseplan_canvas)
        doseplan_text_image_canvas.grid(row=0,column=0,sticky=N+S+W+E)
        doseplan_text_image_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            width=Globals.profiles_doseplan_text_image.width(), height=Globals.profiles_doseplan_text_image.height())

        scaled_image_visual = PIL_img_doseplan_ROI
        scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
        Globals.doseplan_write_image_width = scaled_image_visual.width()
        Globals.doseplan_write_image_height = scaled_image_visual.height()
        Globals.doseplan_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
        Globals.doseplan_write_image.image = scaled_image_visual
        doseplan_text_image_canvas.create_image(0,0,image=Globals.profiles_doseplan_text_image, anchor="nw")
        doseplan_text_image_canvas.image=Globals.profiles_doseplan_text_image

        Globals.profiles_doseplan_dataset_ROI = doseplan_ROI

        Globals.profiles_upload_button_doseplan.config(state=DISABLED)

        several_doseplans_window.after(500, lambda: several_doseplans_window.destroy())
        drawProfiles(False)

    doseplans_done_button_frame = tk.Frame(Globals.doseplans_scroll_frame)
    doseplans_done_button_frame.grid(row=0, column = 1, padx=(0,40), pady=(30,0), sticky=N+S+W+E)
    doseplans_done_button_frame.config(bg='#ffffff')
    Globals.doseplans_scroll_frame.grid_rowconfigure(3, weight=0)
    Globals.doseplans_scroll_frame.grid_columnconfigure(3, weight=0)

    doseplans_done_button = tk.Button(doseplans_done_button_frame, text='Done', image=Globals.done_button_image,\
        cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=closeUploadDoseplans)
    doseplans_done_button.pack(expand=True, fill=BOTH)
    doseplans_done_button.configure(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
    doseplans_done_button.image = Globals.done_button_image
    

    filename_title = tk.Text(Globals.doseplans_scroll_frame, width = 15, height= 1)
    filename_title.insert(INSERT, "Filename")
    filename_title.grid(row=2, column=0, sticky=N+S+E+W, pady=(40,0), padx=(45,15))
    filename_title.config(bg='#ffffff', relief=FLAT, state=DISABLED, font=('calibri', '15', 'bold'))
    Globals.doseplans_scroll_frame.grid_rowconfigure(1, weight=0)
    Globals.doseplans_scroll_frame.grid_columnconfigure(1, weight=0)

    factor_title = tk.Text(Globals.doseplans_scroll_frame, width=30, height=2)
    factor_title.insert(INSERT, "Here you can write a factor to use \non the doseplan. Defaults to 1.")
    factor_title.grid(row=2, column=1, sticky=N+W+S+E, pady=(37,10), padx=(15,25))
    factor_title.config(bg='#ffffff', relief=FLAT, state=DISABLED, font=('calibri', '15', 'bold'))
    Globals.doseplans_scroll_frame.grid_columnconfigure(2,weight=0)
    Globals.doseplans_scroll_frame.grid_rowconfigure(2, weight=0)



def UploadDoseplan(only_one):
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
    try:
        dose_summation_type = dataset.DoseSummationType
    except:
        messagebox.showerror("Error", "Could not upload the doseplan correctly. Try again or another file.\n (Code: dose summation)")
        return
    
    if(not(dose_summation_type == "PLAN")):
        ok = messagebox.askokcancel("Dose summation", "You did not upload the full doseplan. Do you want to continue?")
        if not ok:
            return
    os.chdir(current_folder)
    doseplan_dataset = dataset.pixel_array
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
        return
    
    if not only_one and Globals.profiles_number_of_doseplans > 1:
        if(not (Globals.profiles_dataset_doseplan.PixelSpacing==dataset.PixelSpacing)):
            messagebox.showerror("Error", "Resolution of the doseplans must be equal. \n(Code: UploadDoseplan)")
            return
        if(not (Globals.profiles_dataset_doseplan.DoseGridScaling == dataset.DoseGridScaling)):
            messagebox.showerror("Error", "Dose grid scaling of the doseplans must be equal. \n(Code: UploadDoseplan)")
            return
    Globals.profiles_dataset_doseplan = dataset
    Globals.profiles_dose_scaling_doseplan = dataset.DoseGridScaling
    Globals.profiles_test_if_added_doseplan = True
    if(Globals.profiles_test_if_added_rtplan):
        if(Globals.profiles_isocenter_or_reference_point == "Isocenter"):
            processDoseplan_usingIsocenter(only_one)
        elif(Globals.profiles_isocenter_or_reference_point == "Ref_point"):
            processDoseplan_usingReferencePoint(only_one)
        else:
            messagebox.showerror("Error", "Something went wrong. Try again.\n (Code: processDoseplan)")
            return

    if only_one:
        Globals.profiles_upload_button_doseplan.config(state=DISABLED)

    if not only_one:
        filename = basename(normpath(file))
        textbox_filename = tk.Text(Globals.doseplans_scroll_frame, width = 30, height = 1)
        textbox_filename.insert(INSERT, filename)
        textbox_filename.config(bg='#ffffff', font=('calibri', '12'), state=DISABLED, relief=FLAT)
        textbox_filename.grid(row = Globals.profiles_number_of_doseplans_row_count, column = 0, sticky=N+S+W+E, pady=(10,10), padx=(10,10))
        Globals.doseplans_scroll_frame.grid_columnconfigure(Globals.profiles_doseplans_grid_config_count, weight=0)
        Globals.doseplans_scroll_frame.grid_rowconfigure(Globals.profiles_doseplans_grid_config_count, weight=0)
        Globals.profiles_doseplans_filenames.append(textbox_filename)

        Globals.profiles_doseplans_grid_config_count+=1;

        textbox_factor = tk.Text(Globals.doseplans_scroll_frame, width = 6, height = 1)
        textbox_factor.insert(INSERT, "Factor: ")
        textbox_factor.config(bg='#ffffff', font=('calibri', '12'), state=DISABLED, relief=FLAT)
        textbox_factor.grid(row = Globals.profiles_number_of_doseplans_row_count, column = 1, sticky=N+S+W+E, pady=(10,10), padx=(10,10))
        Globals.doseplans_scroll_frame.grid_columnconfigure(Globals.profiles_doseplans_grid_config_count, weight=0)
        Globals.doseplans_scroll_frame.grid_rowconfigure(Globals.profiles_doseplans_grid_config_count, weight=0)
        Globals.profiles_doseplans_factor_text.append(textbox_factor)

        Globals.profiles_doseplans_grid_config_count+=1;

        textbox_factor_input = tk.Text(Globals.doseplans_scroll_frame)
        textbox_factor_input.insert(INSERT, " ")
        textbox_factor_input.config(bg='#E5f9ff', font=('calibri', '12'), state=NORMAL, bd = 2)
        textbox_factor_input.grid(row = Globals.profiles_number_of_doseplans_row_count, column = 1, sticky=N+S+W+E, pady=(10,10), padx=(30,10))
        Globals.doseplans_scroll_frame.grid_columnconfigure(Globals.profiles_doseplans_grid_config_count, weight=0)
        Globals.doseplans_scroll_frame.grid_rowconfigure(Globals.profiles_doseplans_grid_config_count, weight=0)
        Globals.profiles_doseplans_factor_input.append(textbox_factor_input)

        Globals.profiles_number_of_doseplans_row_count+=1
        Globals.profiles_doseplans_grid_config_count+=1;


######################################################## F I L M ########################################################
def markIsocenter(img, new_window_isocenter_tab, image_canvas, cv2Img):
    if(len(Globals.profiles_mark_isocenter_oval)>0):
        image_canvas.delete(Globals.profiles_mark_isocenter_up_down_line[0])
        image_canvas.delete(Globals.profiles_mark_isocenter_right_left_line[0])
        image_canvas.delete(Globals.profiles_mark_isocenter_oval[0])

        Globals.profiles_mark_isocenter_oval=[]
        Globals.profiles_mark_isocenter_right_left_line=[]
        Globals.profiles_mark_isocenter_up_down_line=[]

    Globals.profiles_iscoenter_coords = []
    img_mark_isocenter = ImageTk.PhotoImage(image=img)
    mark_isocenter_window = tk.Toplevel(new_window_isocenter_tab)
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
    mark_isocenter_image_canvas.config(cursor='hand2', bg='#ffffff', relief=FLAT, bd=0, \
        scrollregion=mark_isocenter_image_canvas.bbox(ALL), height=img_mark_isocenter.height(), width=img_mark_isocenter.width())
    mark_isocenter_image_canvas.grid_propagate(0)

    def findCoords(event):
        mark_isocenter_image_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        if(Globals.profiles_iscoenter_coords==[]):
            Globals.profiles_iscoenter_coords.append([event.x, event.y])
            mark_isocenter_image_canvas.config(cursor='hand2')

        elif(len(Globals.profiles_iscoenter_coords)==1):
            Globals.profiles_iscoenter_coords.append([event.x, event.y])
            Globals.profiles_film_isocenter = [Globals.profiles_iscoenter_coords[0][0], Globals.profiles_iscoenter_coords[1][1]]
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
            
    mark_isocenter_image_canvas.bind("<Button 1>",findCoords)

    
def markReferencePoint(img, new_window_reference_point_tab, image_canvas_reference_tab, cv2Img):

    if(len(Globals.profiles_mark_reference_point_oval)>0):
        image_canvas_reference_tab.delete(Globals.profiles_mark_reference_point_oval[0])
        Globals.profiles_mark_reference_point_oval=[]
     
    img_mark_reference_point = ImageTk.PhotoImage(image=img)
    mark_reference_point_window = tk.Toplevel(new_window_reference_point_tab)
    mark_reference_point_window.geometry("1035x620+10+10")
    mark_reference_point_window.grab_set()

    mark_reference_point_over_all_frame = tk.Frame(mark_reference_point_window, bd=0, relief=FLAT)
    mark_reference_point_over_all_canvas = Canvas(mark_reference_point_over_all_frame)

    mark_reference_point_xscrollbar = Scrollbar(mark_reference_point_over_all_frame, orient=HORIZONTAL, command=mark_reference_point_over_all_canvas.xview)
    mark_reference_point_yscrollbar = Scrollbar(mark_reference_point_over_all_frame, command=mark_reference_point_over_all_canvas.yview)

    mark_reference_point_scroll_frame = ttk.Frame(mark_reference_point_over_all_canvas)
    mark_reference_point_scroll_frame.bind("<Configure>", lambda e: mark_reference_point_over_all_canvas.configure(scrollregion=mark_reference_point_over_all_canvas.bbox('all')))

    mark_reference_point_over_all_canvas.create_window((0,0), window=mark_reference_point_scroll_frame, anchor='nw')
    mark_reference_point_over_all_canvas.configure(xscrollcommand=mark_reference_point_xscrollbar.set, yscrollcommand=mark_reference_point_yscrollbar.set)

    mark_reference_point_over_all_frame.config(highlightthickness=0, bg='#ffffff')
    mark_reference_point_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
    mark_reference_point_over_all_frame.pack(expand=True, fill=BOTH)
    mark_reference_point_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
    mark_reference_point_over_all_frame.grid_columnconfigure(0, weight=1)
    mark_reference_point_over_all_frame.grid_rowconfigure(0, weight=1)
    mark_reference_point_xscrollbar.grid(row=1, column=0, sticky=E+W)
    mark_reference_point_over_all_frame.grid_columnconfigure(1, weight=0)
    mark_reference_point_over_all_frame.grid_rowconfigure(1, weight=0)
    mark_reference_point_yscrollbar.grid(row=0, column=1, sticky=N+S)
    mark_reference_point_over_all_frame.grid_columnconfigure(2, weight=0)
    mark_reference_point_over_all_frame.grid_rowconfigure(2, weight=0)

    mark_reference_point_image_canvas = tk.Canvas(mark_reference_point_scroll_frame)
    mark_reference_point_image_canvas.grid(row=0,column=0, rowspan=10, columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
    mark_reference_point_scroll_frame.grid_columnconfigure(0, weight=0)
    mark_reference_point_scroll_frame.grid_rowconfigure(0, weight=0)

    mark_reference_point_image_canvas.create_image(0,0,image=img_mark_reference_point,anchor="nw")
    mark_reference_point_image_canvas.image = img_mark_reference_point
    mark_reference_point_image_canvas.config(cursor='hand2', bg='#ffffff', relief=FLAT, bd=0, \
        scrollregion=mark_reference_point_image_canvas.bbox(ALL), height=img_mark_reference_point.height(), width=img_mark_reference_point.width())
    mark_reference_point_image_canvas.grid_propagate(0)


    def findCoords(event):
        mark_reference_point_image_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        Globals.profiles_film_reference_point = [event.x, event.y]
        oval = image_canvas_reference_tab.create_oval(int(Globals.profiles_film_reference_point[0]/2)-3, \
            int(Globals.profiles_film_reference_point[1]/2)-3, int(Globals.profiles_film_reference_point[0]/2)+3, \
            int(Globals.profiles_film_reference_point[1]/2)+3, fill='red')
        Globals.profiles_mark_reference_point_oval.append(oval)

        mark_reference_point_window.after(500, lambda: mark_reference_point_window.destroy())
        Globals.profiles_reference_point_check = True
        if(Globals.profiles_ROI_reference_point_check):
            Globals.profiles_done_button_reference_point.config(state=ACTIVE)

    mark_reference_point_image_canvas.bind("<Button 1>",findCoords)

def markROI(img, tab, canvas, ref_point_test):
    if(len(Globals.profiles_mark_ROI_rectangle)>0):
        canvas.delete(Globals.profiles_mark_ROI_rectangle[0])
        Globals.profiles_mark_ROI_rectangle = []

    Globals.profiles_ROI_coords = []

    img_mark_ROI = ImageTk.PhotoImage(image=img)
    mark_ROI_window = tk.Toplevel(tab)
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

        rect = canvas.create_rectangle(int((rectangle_top_corner[0][0])/2), int((rectangle_top_corner[0][1])/2),\
            int((rectangle_bottom_corner[0][0])/2), int((rectangle_bottom_corner[0][1])/2), outline='Blue', width=2)
        Globals.profiles_mark_ROI_rectangle.append(rect)

        if(ref_point_test):
            Globals.profiles_ROI_reference_point_check = True
            if(Globals.profiles_reference_point_check):
                Globals.profiles_done_button_reference_point.config(state=ACTIVE)
        else:
            Globals.profiles_ROI_check = True
            if(Globals.profiles_isocenter_check):
                Globals.profiles_done_button.config(state=ACTIVE)


        mark_ROI_window.after(500, lambda: mark_ROI_window.destroy())

    mark_ROI_image_canvas.bind("<B1-Motion>", buttonMoving)
    mark_ROI_image_canvas.bind("<Button-1>", buttonPushed)
    mark_ROI_image_canvas.bind("<ButtonRelease-1>", buttonReleased)


def UploadFilm():
    if(Globals.profiles_film_orientation.get() == '-'):
        messagebox.showerror("Missing parameter", "Film orientation missing \n (Code: UploadFilm)")
        return
    if Globals.profiles_film_factor_input.get("1.0", 'end-1c') == " ":
        Globals.profiles_film_factor = 1
    else:
        try:
            Globals.profiles_film_factor = float(Globals.profiles_film_factor_input.get("1.0", 'end-1c'))
        except:
            messagebox.showerror("Missing parameter", "Film factor invalid format. \n (Code: UploadFilm)")
            return

    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(ext == '.tif'):
        current_folder = os.getcwd()
        parent = os.path.dirname(file)
        os.chdir(parent)
        img = Image.open(file)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        cv2Img = cv2.imread(basename(normpath(file)), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        cv2Img = cv2.medianBlur(cv2Img, 5)
        if(cv2Img is None):
            messagebox.showerror("Error", "Something has gone wrong. Check that the filename does not contain Æ,Ø,Å")
            return
        if(cv2Img.shape[2] == 3):
            if(cv2Img.shape[0]==1270 and cv2Img.shape[1]==1016):
                cv2Img = abs(cv2Img-Globals.correctionMatrix127)
                cv2Img = np.clip(cv2Img, 0, 65535)
                cv2Img = cv2.flip(cv2Img,1)
                img_scaled = img.resize((508, 635), Image.ANTIALIAS)
                img_scaled = ImageTk.PhotoImage(image=img_scaled)
                

                Globals.profiles_film_dataset = cv2Img
                Globals.profiles_film_dataset_red_channel = cv2Img[:,:,2]
            else:
                messagebox.showerror("Error","The resolution of the image is not consistent with dpi")
                return
        else:
            messagebox.showerror("Error","The uploaded image need to be in RGB-format")
            return

        os.chdir(current_folder)  
       
        if(not (img.width == 1016)):
            messagebox.showerror("Error", "Dpi in image has to be 127")
            return

        Globals.profiles_film_orientation_menu.configure(state=DISABLED)
        Globals.profiles_film_factor_input.config(state=DISABLED)
    
        h = 635 + 20
        w = 508 + 625
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

        new_window_explain_text = tk.Text(new_window_scroll_frame, height= 3, width=120)
        new_window_explain_text.insert(INSERT, \
"To match the film with the doseplan you have to mark either isocenter or a reference point\
on the film of your choice.In the case of the reference point you \nwill be asked to input the \
lenght in lateral, longitudinal and vertical to a reference point used in the linac. It the \
reference point in the film is the same as \nthe one in the phantom/linac you can input all zeros,\
in other cases your input is in mm. Later you will have the oppertunity to make small\
adjustments \nto the placement of either the reference point or isocenter.")
        new_window_explain_text.config(state=DISABLED, font=('calibri', '13', 'bold'), bg = '#ffffff', relief=FLAT)
        new_window_explain_text.grid(row=0, column=0, columnspan=5, sticky=N+S+W+E, pady=(15,5), padx=(10,10))
        new_window_scroll_frame.grid_rowconfigure(0, weight=0)
        new_window_scroll_frame.grid_columnconfigure(0, weight=0)

        new_window_notebook = ttk.Notebook(new_window_scroll_frame)
        new_window_notebook.borderWidth=0
        new_window_notebook.grid(row=2, column=0, columnspan=5, sticky=E+W+N+S, pady=(0,0), padx =(0,0))
        new_window_scroll_frame.grid_rowconfigure(4, weight=0)
        new_window_scroll_frame.grid_columnconfigure(4, weight=0)

        new_window_isocenter_tab = ttk.Frame(new_window_notebook)
        new_window_notebook.add(new_window_isocenter_tab, text='Isocenter')
        new_window_reference_point_tab = ttk.Frame(new_window_notebook)
        new_window_notebook.add(new_window_reference_point_tab, text='Reference point')
        new_window_manually_tab = ttk.Frame(new_window_notebook)
        new_window_notebook.add(new_window_manually_tab, text='Manually')


        image_canvas = tk.Canvas(new_window_isocenter_tab)
        image_canvas.grid(row=0,column=0, rowspan=12, columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
        new_window_isocenter_tab.grid_rowconfigure(1, weight=0)
        new_window_isocenter_tab.grid_columnconfigure(1, weight=0)
        image_canvas.create_image(0,0,image=img_scaled,anchor="nw")
        image_canvas.image = img_scaled
        image_canvas.config(bg='#ffffff', relief=FLAT, bd=0, scrollregion=image_canvas.bbox(ALL), \
            height=img_scaled.height(), width=img_scaled.width())
        image_canvas.grid_propagate(0)

        image_canvas_reference_tab = tk.Canvas(new_window_reference_point_tab)
        image_canvas_reference_tab.grid(row=0,column=0, rowspan=10, columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
        new_window_reference_point_tab.grid_rowconfigure(1, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(1, weight=0)
        image_canvas_reference_tab.create_image(0,0,image=img_scaled,anchor="nw")
        image_canvas_reference_tab.image = img_scaled
        image_canvas_reference_tab.config(bg='#ffffff', relief=FLAT, bd=0, scrollregion=image_canvas.bbox(ALL), \
            height=img_scaled.height(), width=img_scaled.width())
        image_canvas_reference_tab.grid_propagate(0)

        film_window_mark_isocenter_text = tk.Text(new_window_isocenter_tab, width=55, height=7)
        film_window_mark_isocenter_text.insert(INSERT, \
"When clicking the button \"Mark isocenter\" a window showing \n\
the image will appear and you are to click on the markers \n\
made on the film upon irradiation to find the isocenter. Start \n\
with the marker showing the direction of the film (see the \n\
specifications in main window). When both marks are made \n\
you will see the isocenter in the image. If you are not happy \n\
with the placement click the button again and repeat.")
        film_window_mark_isocenter_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_isocenter_text.grid(row=0, column=3, rowspan=3, sticky=N+S+E+W, padx=(10,10), pady=(10,0))
        new_window_isocenter_tab.columnconfigure(2, weight=0)
        new_window_isocenter_tab.rowconfigure(2, weight=0)

        film_window_mark_reference_point_text = tk.Text(new_window_reference_point_tab, width=55, height=5)
        film_window_mark_reference_point_text.insert(INSERT, \
"When clicking the button \"Mark point\" a window showing \n\
the image will appear and you are to click on the marker \n\
made on the film upon irradiation to find the point. When\n\
the mark are made you will see the isocenter in the image.\n\
If you are not happy with the placement click the button \n\
again and repeat.")
        film_window_mark_reference_point_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_reference_point_text.grid(row=0, column=3, rowspan=3, sticky=N+S+E+W, padx=(10,10), pady=(5,0))
        new_window_reference_point_tab.columnconfigure(2, weight=0)
        new_window_reference_point_tab.rowconfigure(2, weight=0)
            
        mark_isocenter_button_frame = tk.Frame(new_window_isocenter_tab)
        mark_isocenter_button_frame.grid(row=3, column=3, padx=(10,10), pady=(0,10))
        mark_isocenter_button_frame.configure(bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(3, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(3, weight=0)

        mark_isocenter_button = tk.Button(mark_isocenter_button_frame, text='Browse', image=Globals.profiles_mark_isocenter_button_image,\
            cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: markIsocenter(img, new_window_isocenter_tab, image_canvas, cv2Img))
        mark_isocenter_button.pack(expand=True, fill=BOTH)
        mark_isocenter_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        mark_isocenter_button.image=Globals.profiles_mark_isocenter_button_image

        mark_point_button_frame = tk.Frame(new_window_reference_point_tab)
        mark_point_button_frame.grid(row=3, column=3, padx=(10,10), pady=(30,0))
        mark_point_button_frame.configure(bg='#ffffff')
        new_window_reference_point_tab.grid_columnconfigure(3, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(3, weight=0)

        mark_point_button = tk.Button(mark_point_button_frame, text='Browse', image=Globals.profiles_mark_point_button_image,\
            cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: \
                markReferencePoint(img, new_window_reference_point_tab, image_canvas_reference_tab, cv2Img))
        mark_point_button.pack(expand=True, fill=BOTH)
        mark_point_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        mark_point_button.image=Globals.profiles_mark_point_button_image

        write_displacement_relative_to_reference_point = tk.Text(new_window_reference_point_tab, width = 55, height=3)
        write_displacement_relative_to_reference_point.insert(INSERT, "\
If the marked reference points in the film does not match\n\
the reference point in the phantom you can write the\n\
displacemnet here (in mm). Defaults to zero ")
        write_displacement_relative_to_reference_point.grid(row=4, column=3, rowspan=2, sticky=N+S+E+W, padx=(10,10), pady=(0,10))
        write_displacement_relative_to_reference_point.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        new_window_reference_point_tab.grid_rowconfigure(6, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(6, weight=0)

        input_lateral_text = tk.Text(new_window_reference_point_tab, width=12, height=1)
        input_lateral_text.insert(INSERT, "Lateral:")
        input_lateral_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '10'))
        input_lateral_text.grid(row=5, column=3, sticky=N+S, padx=(0,250), pady=(25,0))
        new_window_reference_point_tab.grid_rowconfigure(10, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(10, weight=0)

        Globals.profiles_input_lateral_displacement = tk.Text(new_window_reference_point_tab, width=5, height=1)
        Globals.profiles_input_lateral_displacement.insert(INSERT, " ")
        Globals.profiles_input_lateral_displacement.config(bg='#E5f9ff', relief=GROOVE, bd=2, state=NORMAL, font=('calibri', '11'))
        Globals.profiles_input_lateral_displacement.grid(row=5, column=3, padx=(0,285), pady=(35,0))
        new_window_reference_point_tab.grid_rowconfigure(7, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(7, weight=0)

        input_vertical_text = tk.Text(new_window_reference_point_tab, width=12, height=1)
        input_vertical_text.insert(INSERT, "Vertical:")
        input_vertical_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '10'))
        input_vertical_text.grid(row=5, column=3, sticky=N+S, padx=(0,0), pady=(25,0))
        new_window_reference_point_tab.grid_rowconfigure(11, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(11, weight=0)

        Globals.profiles_input_vertical_displacement = tk.Text(new_window_reference_point_tab, width=4, height=1)
        Globals.profiles_input_vertical_displacement.insert(INSERT, " ")
        Globals.profiles_input_vertical_displacement.config(bg='#E5f9ff', relief=GROOVE, bd=2, state=NORMAL, font=('calibri', '11'))
        Globals.profiles_input_vertical_displacement.grid(row=5, column=3, padx=(0,25), pady=(35,0))
        new_window_reference_point_tab.grid_rowconfigure(8, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(8, weight=0)   

        input_long_text = tk.Text(new_window_reference_point_tab, width=12, height=1)
        input_long_text.insert(INSERT, "Longitudinal:")
        input_long_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '10'))
        input_long_text.grid(row=5, column=3, sticky=N+S, padx=(250,0), pady=(25,0))
        new_window_reference_point_tab.grid_rowconfigure(12, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(12, weight=0)

        Globals.profiles_input_longitudinal_displacement = tk.Text(new_window_reference_point_tab, width=5, height=1)
        Globals.profiles_input_longitudinal_displacement.insert(INSERT, " ")
        Globals.profiles_input_longitudinal_displacement.config(bg='#E5f9ff', relief=GROOVE, bd=2, state=NORMAL, font=('calibri', '11'))
        Globals.profiles_input_longitudinal_displacement.grid(row=5, column=3, padx=(240,0), pady=(35,0))
        new_window_reference_point_tab.grid_rowconfigure(9, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(9, weight=0)     

        film_window_mark_ROI_text = tk.Text(new_window_isocenter_tab, width=55, height=7)
        film_window_mark_ROI_text.insert(INSERT, \
"When clicking the button \"Mark ROI\" a window showing the\n\
image will appear and you are to drag a rectangle marking \n\
the region of interest. Fidora will assume the film has been\n\
scanned in either portrait or landscape orientation. When\n\
the ROI has been marked it will appear on the image. If you\n\
are not happy with the placement click the button again.")
        film_window_mark_ROI_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_ROI_text.grid(row=5, column=3, rowspan=4, sticky=N+S+E+W, padx=(10,10), pady=(0,0))
        new_window_isocenter_tab.grid_columnconfigure(4, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(4, weight=0)
        
        film_window_mark_ROI_reference_point_text = tk.Text(new_window_reference_point_tab, width=55, height=5)
        film_window_mark_ROI_reference_point_text.insert(INSERT, \
"When clicking the button \"Mark ROI\" a window showing the\n\
image will appear and you are to drag a rectangle marking \n\
the region of interest. Fidora will assume the film has been\n\
scanned in either portrait or landscape orientation. When\n\
the ROI has been marked it will appear on the image. If you\n\
are not happy with the placement click the button again.")
        film_window_mark_ROI_reference_point_text.config(bg='#ffffff', relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_ROI_reference_point_text.grid(row=6, column=3, rowspan=3, sticky=N+E+W, padx=(10,10), pady=(10,0))
        new_window_reference_point_tab.grid_columnconfigure(4, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(4, weight=0)
        
        mark_ROI_button_frame = tk.Frame(new_window_isocenter_tab)
        mark_ROI_button_frame.grid(row=8, column=3, padx=(10,0), pady=(0,5))
        mark_ROI_button_frame.configure(bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(5, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(5, weight=0)

        mark_ROI_button = tk.Button(mark_ROI_button_frame, text='Browse', image=Globals.profiles_mark_ROI_button_image,\
            cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: markROI(img, new_window_isocenter_tab, image_canvas, False))
        mark_ROI_button.pack(expand=True, fill=BOTH)
        mark_ROI_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        mark_ROI_button.image=Globals.profiles_mark_ROI_button_image

        slice_offset_text = tk.Text(new_window_isocenter_tab, width=25, height=1)
        slice_offset_text.insert(INSERT, "Slice offset, mm (default 0):")
        slice_offset_text.config(state=DISABLED, font=('calibri', '10'), bd = 0, relief=FLAT)   
        slice_offset_text.grid(row=9, column=3, padx=(5,110), pady=(0,0))
        new_window_isocenter_tab.grid_columnconfigure(6, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(6, weight=0)

        Globals.profiles_slice_offset = tk.Text(new_window_isocenter_tab, width=8, height=1)
        Globals.profiles_slice_offset.grid(row=9, column=3, padx=(110,10), pady=(0,0))
        Globals.profiles_slice_offset.insert(INSERT, " ")
        Globals.profiles_slice_offset.config(state=NORMAL, font=('calibri', '10'), bd = 2, bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(7, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(7, weight=0)

        mark_ROI_button_reference_point_frame = tk.Frame(new_window_reference_point_tab)
        mark_ROI_button_reference_point_frame.grid(row=9, column=3, padx=(10,10), pady=(0,5))
        mark_ROI_button_reference_point_frame.configure(bg='#ffffff')
        new_window_reference_point_tab.grid_columnconfigure(5, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(5, weight=0)

        mark_ROI_reference_point_button = tk.Button(mark_ROI_button_reference_point_frame, text='Browse', image=Globals.profiles_mark_ROI_button_image,\
            cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: markROI(img, new_window_reference_point_tab, image_canvas_reference_tab, True))
        mark_ROI_reference_point_button.pack(expand=True, fill=BOTH)
        mark_ROI_reference_point_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        mark_ROI_reference_point_button.image=Globals.profiles_mark_ROI_button_image

        def finishFilmMarkers(ref_test):
            Globals.profiles_slice_offset.config(state=DISABLED)
            if(ref_test):
                if(not(Globals.profiles_input_lateral_displacement.get("1.0",'end-1c')==" ")):
                    try:
                        test = float(Globals.profiles_input_lateral_displacement.get("1.0",'end-1c'))
                        Globals.profiles_lateral = test
                    except:
                        messagebox.showerror("Error", "The displacements must be numbers\n (Code: lateral displacement)")
                        return
                else:
                    Globals.profiles_lateral = 0
                if(not(Globals.profiles_input_longitudinal_displacement.get("1.0",'end-1c')==" ")):
                    try:
                        test = float(Globals.profiles_input_longitudinal_displacement.get("1.0", 'end-1c'))
                        Globals.profiles_longitudinal = test
                    except:
                        messagebox.showerror("Error", "The displacements must be numbers\n (Code: longitudinal displacement)")
                        return
                else:
                    Globals.profiles_longitudinal = 0
                if(not(Globals.profiles_input_vertical_displacement.get("1.0",'end-1c')==" ")):
                    try:
                        test = float(Globals.profiles_input_vertical_displacement.get("1.0", 'end-1c'))
                        Globals.profiles_vertical = test
                    except:
                        messagebox.showerror("Error", "The displacements must be numbers\n (Code: vertical displacement)")
                        return
                else:
                    Globals.profiles_vertical = 0
                Globals.profiles_input_vertical_displacement.config(state=DISABLED)
                Globals.profiles_input_longitudinal_displacement.config(state=DISABLED)
                Globals.profiles_input_lateral_displacement.config(state=DISABLED)
            else:
                if not Globals.profiles_slice_offset.get("1.0",'end-1c')==" ":
                    try:
                        offset = float(Globals.profiles_slice_offset.get("1.0",'end-1c'))
                        Globals.profiles_offset = offset
                    except:
                        messagebox.showerror("Error", "Slice offset must be a number \n(Code: finishFilmMarkers(false)")
                        return
                else:
                    Globals.profiles_offset = 0
            if(ref_test):
                choose_batch_window = tk.Toplevel(new_window_reference_point_tab)
            else:
                choose_batch_window = tk.Toplevel(new_window_isocenter_tab)

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
                        Globals.profiles_film_dataset_ROI_red_channel_dose[i,j] = Globals.profiles_film_factor*\
                            pixel_to_dose(Globals.profiles_film_dataset_ROI_red_channel[i,j], \
                            Globals.profiles_popt_red[0], Globals.profiles_popt_red[1], Globals.profiles_popt_red[2])

                Globals.profiles_film_dataset_red_channel_dose = np.zeros((Globals.profiles_film_dataset_red_channel.shape[0],\
                    Globals.profiles_film_dataset_red_channel.shape[1]))
                for i in range(Globals.profiles_film_dataset_red_channel_dose.shape[0]):
                    for j in range(Globals.profiles_film_dataset_red_channel_dose.shape[1]):
                        Globals.profiles_film_dataset_red_channel_dose[i,j] = Globals.profiles_film_factor*\
                            pixel_to_dose(Globals.profiles_film_dataset_red_channel[i,j], \
                            Globals.profiles_popt_red[0], Globals.profiles_popt_red[1], Globals.profiles_popt_red[2])

                Globals.film_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
                Globals.film_write_image.image = scaled_image_visual

                mx_film=np.max(Globals.profiles_film_dataset_ROI_red_channel_dose)
                Globals.profiles_max_dose_film = mx_film
                img_film = Globals.profiles_film_dataset_ROI_red_channel_dose
                img_film = img_film/mx_film
                PIL_img_film = Image.fromarray(np.uint8(cm.viridis(img_film)*255))

                scaled_image_visual_film = ImageTk.PhotoImage(image=PIL_img_film)
                Globals.film_dose_write_image.create_image(0,0,image=scaled_image_visual_film, anchor="nw")
                Globals.film_dose_write_image.image = scaled_image_visual_film

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
            

            img_ROI = Globals.profiles_film_dataset[Globals.profiles_ROI_coords[0][1]:Globals.profiles_ROI_coords[2][1],\
                Globals.profiles_ROI_coords[0][0]:Globals.profiles_ROI_coords[1][0], :]
            img_ROI_red_channel = img_ROI[:,:,2]
            Globals.profiles_film_variable_ROI_coords = [Globals.profiles_ROI_coords[0][1], Globals.profiles_ROI_coords[2][1],\
                Globals.profiles_ROI_coords[0][0], Globals.profiles_ROI_coords[1][0]]
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

            film_dose_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
            film_dose_canvas.grid(row=1,column=0, sticky=N+S+W+E)
            Globals.profiles_film_panedwindow.add(film_dose_canvas, \
                height=max(heig,Globals.profiles_film_dose_map_text_image.height()), \
                    width=wid + Globals.profiles_film_dose_map_text_image.width())
            film_dose_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
                height=max(heig,Globals.profiles_film_dose_map_text_image.height()), \
                    width=wid + Globals.profiles_film_dose_map_text_image.width())

            Globals.film_write_image = tk.Canvas(film_image_canvas)
            Globals.film_write_image.grid(row=0,column=1,sticky=N+S+W+E)
            Globals.film_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)
            
            Globals.film_dose_write_image = tk.Canvas(film_dose_canvas)
            Globals.film_dose_write_image.grid(row=0,column=1,sticky=N+S+W+E)
            Globals.film_dose_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)           

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

            Globals.profiles_upload_button_doseplan.config(state=DISABLED)
            Globals.profiles_upload_button_rtplan.config(state=ACTIVE)
            Globals.profiles_upload_button_film.config(state=DISABLED)

            #Beregne avstand mellom ROI og isocenter gitt i mm 
            # [top left[mot venstre, oppover], top right[mot venstre (høyre blir negativ), oppover], bottom left, bottom right]
            if(ref_test):
                Globals.profiles_distance_reference_point_ROI.append([(Globals.profiles_film_reference_point[0]-Globals.profiles_ROI_coords[0][0])*0.2, \
                    (Globals.profiles_film_reference_point[1] -Globals.profiles_ROI_coords[0][1])*0.2])
                Globals.profiles_distance_reference_point_ROI.append([(Globals.profiles_film_reference_point[0] - Globals.profiles_ROI_coords[1][0])*0.2,\
                    (Globals.profiles_film_reference_point[1] - Globals.profiles_ROI_coords[1][1])*0.2])
                Globals.profiles_distance_reference_point_ROI.append([(Globals.profiles_film_reference_point[0] - Globals.profiles_ROI_coords[2][0])*0.2,\
                    (Globals.profiles_film_reference_point[1] - Globals.profiles_ROI_coords[2][1])*0.2])
                Globals.profiles_distance_reference_point_ROI.append([(Globals.profiles_film_reference_point[0] - Globals.profiles_ROI_coords[3][0])*0.2,\
                    (Globals.profiles_film_reference_point[1] - Globals.profiles_ROI_coords[3][1])*0.2])
                
                Globals.profiles_isocenter_or_reference_point = "Ref_point"
            else:
                Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0]-Globals.profiles_ROI_coords[0][0])*0.2, \
                    (Globals.profiles_film_isocenter[1] -Globals.profiles_ROI_coords[0][1])*0.2])
                Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0] - Globals.profiles_ROI_coords[1][0])*0.2,\
                    (Globals.profiles_film_isocenter[1] - Globals.profiles_ROI_coords[1][1])*0.2])
                Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0] - Globals.profiles_ROI_coords[2][0])*0.2,\
                    (Globals.profiles_film_isocenter[1] - Globals.profiles_ROI_coords[2][1])*0.2])
                Globals.profiles_distance_isocenter_ROI.append([(Globals.profiles_film_isocenter[0] - Globals.profiles_ROI_coords[3][0])*0.2,\
                    (Globals.profiles_film_isocenter[1] - Globals.profiles_ROI_coords[3][1])*0.2])

                Globals.profiles_isocenter_or_reference_point = "Isocenter"

            
        done_button_frame = tk.Frame(new_window_isocenter_tab)
        done_button_frame.grid(row=10, column=3, padx=(10,10), pady=(5,5), sticky=N+S+W+E)
        done_button_frame.configure(bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(5, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(5, weight=0)

        Globals.profiles_done_button = tk.Button(done_button_frame, text='Done', image=Globals.done_button_image,\
            cursor='hand2', font=('calibri', '14'), relief=FLAT, state=DISABLED, command=lambda: finishFilmMarkers(False))
        Globals.profiles_done_button.pack(expand=True, fill=BOTH)
        Globals.profiles_done_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        Globals.profiles_done_button.image=Globals.done_button_image

        done_button_reference_point_frame = tk.Frame(new_window_reference_point_tab)
        done_button_reference_point_frame.grid(row=10, column=3, padx=(10,10), pady=(5,5), sticky=N+S+W+E)
        done_button_reference_point_frame.configure(bg='#ffffff')
        new_window_reference_point_tab.grid_columnconfigure(5, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(5, weight=0)

        Globals.profiles_done_button_reference_point= tk.Button(done_button_reference_point_frame, text='Done', image=Globals.done_button_image,\
            cursor='hand2', font=('calibri', '14'), relief=FLAT, state=DISABLED, command=lambda: finishFilmMarkers(True))
        Globals.profiles_done_button_reference_point.pack(expand=True, fill=BOTH)
        Globals.profiles_done_button_reference_point.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
        Globals.profiles_done_button_reference_point.image=Globals.done_button_image


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
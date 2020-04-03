import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
    PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE, ACTIVE, \
    FLAT, END, Scrollbar, HORIZONTAL, VERTICAL, ttk
import os
from os.path import normpath, basename
from PIL import Image, ImageTk
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import pydicom
import numpy as np
from matplotlib.figure import Figure
import matplotlib as mpl
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
    else:
        file = filedialog.askopenfilename()
        ext = os.path.splitext(file)[-1].lower()
        if(ext=='.dcm'):
            doseplan_dataset = pydicom.dcmread(file)
            doseplan_dataset_pixelArray = doseplan_dataset.pixel_array

            ############################ Her må vi senere legge inn posisjon på en eller annen måte! #########################
            doseplan = doseplan_dataset_pixelArray[30,:,:]

            Globals.profiles_doseplan_dataset = doseplan
            doseplan=doseplan_dataset.DoseGridScaling*doseplan*100   #converts from pixel to cGy

            canvas_doseplan = Canvas(Globals.profile_film_visual, bd=0)
            canvas_doseplan.grid(row=1, column=0, sticky=N+S+E+W, pady=(5,0), padx=(100,30))
            Globals.profile_film_visual.grid_columnconfigure(1, weight=0)
            Globals.profile_film_visual.grid_rowconfigure(1, weight=0)
            
            doseplan = 255*doseplan/np.amax(doseplan)
            doseplan = doseplan.astype('uint8')
            img = Image.fromarray(doseplan, mode='P')


            scale_horizontal = 8
            scale_vertical = 10
            img_scaled = img.resize((scale_horizontal*15, scale_vertical*15), Image.ANTIALIAS)
        
            img_scaled = ImageTk.PhotoImage(image=img_scaled)
        

            canvas_doseplan.create_image(0,0,image=img_scaled,anchor="nw")
            canvas_doseplan.image = img_scaled
            canvas_doseplan.config(scrollregion=canvas_doseplan.bbox(ALL), width=120, height=150)

        elif(ext==""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dmc file")
"""

def UploadFilm():
    if(Globals.profiles_film_orientation.get() == '-'):
        messagebox.showerror("Missing parameter", "Film orientation missing")
        return
    if(Globals.profiles_depth.get("1.0",'end-1c') == " "):
        messagebox.showerror("Missing parameter", "Film depth missing")
        return
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
                Globals.profiles_iscoenter_coords.append([event.x, event.y])
                #print(event.x, event.y)
                mark_isocenter_image_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
                if(len(Globals.profiles_iscoenter_coords)==1):
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
                ### Husk at koordinatene går bortover så nedover!
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

            set_batch_button_frame = tk.Frame(choose_batch_frame)
            set_batch_button_frame.grid(row=row_cnt, column=1, columnspan=3, padx=(10,0), pady=(5,5))
            set_batch_button_frame.configure(bg='#ffffff')
            choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
            choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)

            set_batch_button = tk.Button(set_batch_button_frame, text='OK', image=Globals.done_button_image, cursor='hand2',\
                font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=set_batch)
            set_batch_button.pack(expand=True, fill=BOTH)
            set_batch_button.image=Globals.done_button_image
            read.close()
            
            scaled_image_visual = img.resize((8*25, 10*25), Image.ANTIALIAS)
            scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
            Globals.profile_film_visual.create_image(0,0,image=scaled_image_visual,anchor="nw")
            Globals.profile_film_visual.image = scaled_image_visual
            new_window.destroy()

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
    print(Globals.profiles_film_orientation.get())
    return

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

    Globals.profiles_done_button.config(state=DISABLED)
    Globals.profiles_isocenter_check = False
    Globals.profiles_ROI_check = False
    
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
import tkinter as tk
from tkinter import ttk, INSERT, DISABLED, GROOVE, CURRENT, Radiobutton, \
    NORMAL, ACTIVE, messagebox, Menu, IntVar, Checkbutton, FLAT, PhotoImage, Label,\
        SOLID, N, S, W, E, END, LEFT, Scrollbar, RIGHT, Y, BOTH, TOP, OptionMenu, SUNKEN, \
        RIDGE
import Globals
import re
import CoMet_functions, intro_tab_functions, Map_Dose
import Dose_response_functions, Profile_functions
from PIL import Image, ImageTk
import os
import sys



Globals.form.title("FIDORA")
#lobals.form.geometry("1250x600")
Globals.form.configure(bg='#ffffff')
Globals.form.state('zoomed')

Globals.form.tk.call('wm', 'iconphoto', Globals.form._w, PhotoImage(file='logo_fidora.png'))
Globals.form.iconbitmap(default='logo_fidora.png')

load = Image.open("fidora_logo.png")
render = ImageTk.PhotoImage(load)
label = Label(Globals.scroll_frame, image=render)
label.image = render
label.grid(row = 0, column = 0, sticky=W)# place(relwidt=0.61,relheight=0.15, relx=0.02, rely=0.0)
label.config(bg='#FFFFFF') 

Globals.tab_parent.add(Globals.intro_tab, text='FIDORA')
Globals.tab_parent.add(Globals.tab1, text='CoMet')
Globals.tab_parent.add(Globals.tab2, text='Dose-response')
Globals.tab_parent.add(Globals.tab3, text='Map dose')
Globals.tab_parent.add(Globals.tab4, text='Profiles')

style = ttk.Style()
style.theme_create('MyStyle', parent= 'classic', settings={
    ".": {
        "configure": {
            "background": '#FFFFFF', # All colors except for active tab-button
            "font": 'red'
        }
    },
    "Horizontal.TProgressbar":{
        "configure": {
            "background": '#2C8EAD',
            "bordercolor": '#32A9CE',
            "troughcolor": "#ffffff",
        }
    },
    "TNotebook": {
        "configure": {
            "background":'#ffffff', # color behind the notebook
            "tabmargins": [5, 5, 10, 10], # [left margin, upper margin, right margin, margin beetwen tab and frames]
            "tabposition": 'wn',
            "borderwidth": 0,

        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#0A7D76', # Color of non selected tab-button
            "foreground": '#ffffff',
            "padding": [30,35, 20,35], # [space beetwen text and horizontal tab-button border, space between text and vertical tab_button border]
            "font": ('#FFFFFF', '15'),
            "borderwidth": 1,
            "equalTabs": True,
            "width": 13
            
        },
        "map": {
            "background": [("selected", '#02B9A5')], # Color of active tab
            "expand": [("selected", [1, 1, 1, 0])] # [expanse of text]
        }
    }
})

style.theme_use('MyStyle')


menubar = Menu(Globals.form)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Restart", command=CoMet_functions.nothingButton)
filemenu.add_command(label="Open", command=CoMet_functions.nothingButton)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=Globals.form.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=CoMet_functions.nothingButton)
helpmenu.add_command(label="About", command=CoMet_functions.nothingButton)
menubar.add_cascade(label="Help", menu=helpmenu)
Globals.form.config(menu=menubar)

upload_button_file = "uploadbutton3.png" 
Globals.upload_button_image = ImageTk.PhotoImage(file=upload_button_file)

select_folder_button_file = "select_folder_button2.png"
select_folder_image = ImageTk.PhotoImage(file=select_folder_button_file)

help_button_file = "help_button.png"
Globals.help_button = ImageTk.PhotoImage(file=help_button_file)

CoMet_border_dark_file = "border.png"
CoMet_border_dark = ImageTk.PhotoImage(file=CoMet_border_dark_file)

CoMet_border_light_file = "border_light.png"
CoMet_border_light = ImageTk.PhotoImage(file=CoMet_border_light_file)

CoMet_save_button_file = "save_button2.png"
CoMet_save_button = ImageTk.PhotoImage(file=CoMet_save_button_file)
Globals.save_button = ImageTk.PhotoImage(file=CoMet_save_button_file)

CoMet_correct_button_file = "icon_correct.png"
CoMet_correct_button_image= ImageTk.PhotoImage(file=CoMet_correct_button_file)

CoMet_clear_all_button_file = "icon_clear_all.png"
CoMet_clear_all_button_image = ImageTk.PhotoImage(file=CoMet_clear_all_button_file)

dose_response_clear_all_button_file = "icon_clear_all_small.png"
dose_response_clear_all_button_image = ImageTk.PhotoImage(file=dose_response_clear_all_button_file)

CoMet_empty_image_file = "empty_corrected_image.png"
CoMet_empty_image_image = ImageTk.PhotoImage(file=CoMet_empty_image_file)

dose_response_calibration_button_file = "save_calibration_button.png"
dose_response_calibration_button_image = ImageTk.PhotoImage(file=dose_response_calibration_button_file)

dose_response_dose_border_file = "dose_border.png"
Globals.dose_response_dose_border = ImageTk.PhotoImage(file=dose_response_dose_border_file)

profiles_add_doseplan_button_file = "add_doseplan_button.png"
profiles_add_doseplan_button_image = ImageTk.PhotoImage(file=profiles_add_doseplan_button_file)

profiles_add_film_button_file = "add_film_button.png"
profiles_add_film_button_image = ImageTk.PhotoImage(file=profiles_add_film_button_file)

profiles_showPlanes_file = "planes.png"
Globals.profiles_showPlanes_image = ImageTk.PhotoImage(file=profiles_showPlanes_file)

profiles_showDirections_file = 'depth_directions.png'
Globals.profiles_showDirections_image = ImageTk.PhotoImage(file=profiles_showDirections_file)
###################################### INTRO TAB #################################################


#scrollbar = Scrollbar(Globals.intro_tab)
#scrollbar.pack(side=RIGHT, fill=Y)#grid(row=0, column=1, sticky=N+S+E)#pack(side=RIGHT, fill=Y)
#Globals.intro_tab.grid_columnconfigure(0, weight=0)
#Globals.intro_tab.grid_rowconfigure(0, weight=0)
intro_tab_canvas = tk.Canvas(Globals.intro_tab)#, yscrollcommand=scrollbar.set)
intro_tab_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)


tab1_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab1_text_box.grid(row=0, column=0, pady=(30,30), padx=(55,0))
tab1_text_box.config(bd=0, bg='#E5f9ff')


tab1_title_text = tk.Text(tab1_text_box, height=1, width=6)
tab1_title_text.insert(END, "CoMet")
tab1_title_text.grid(in_=tab1_text_box, row=0, column = 0, pady=(15,5), padx=(10,10))
tab1_title_text.config(state=DISABLED, bd=0, bg ='#E5f9ff', fg='#130e07', font=('calibri', '25', 'bold'))
tab1_text_box.grid_columnconfigure(0,weight=1)
tab1_text_box.grid_rowconfigure(0,weight=1)

tab1_text = tk.Text(tab1_text_box, height=4, width=43)
tab1_text.grid(in_=tab1_text_box, row=1, column=0, sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab1_text.insert(INSERT,"Correct your scanned images using CoMet. A method \ndeveloped to correct for non-uniformity introduced\n\
by the scanner. The correction is based on absolute \nsubtraction.")
tab1_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '13'))
tab1_text_box.grid_columnconfigure(1,weight=1)
tab1_text_box.grid_rowconfigure(1,weight=1) 

tab1_readmore_text = tk.Text(tab1_text_box, height=1, width=1)
tab1_readmore_text.grid(row=1, column=0, sticky = N+S+W+E, pady=(65,0), padx = (110,0))
tab1_readmore_text.insert(INSERT,"Read more...")
tab1_readmore_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '12', 'bold')) 
tab1_text_box.grid_columnconfigure(2,weight=1)
tab1_text_box.grid_rowconfigure(2,weight=1)

tab1_box_figure = Image.open("icon_comet.png")
tab1_figure = ImageTk.PhotoImage(tab1_box_figure)
tab1_figure_label = Label(tab1_text_box, image=tab1_figure)
tab1_figure_label.image = tab1_figure
tab1_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab1_figure_label.config(bg='#E5f9ff')
tab1_text_box.grid_columnconfigure(3, weight=1)
tab1_text_box.grid_rowconfigure(3, weight=1)

"""
tab1_readmore = tk.Button(tab1_text_box, text='Read more',cursor='hand2',font=('calibri', '12', 'bold'),\
    relief=FLAT, state=tk.ACTIVE, width = 15, command=intro_tab_functions.readMore)
tab1_readmore.place(relwidth=0.25, relheight=0.13, relx=0.27, rely=0.054)
"""
tab2_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab2_text_box.grid(row=0, column=1, pady=(30,30), padx=(65,0))
tab2_text_box.config(bd=0, bg='#E5f9ff')

tab2_title = tk.Text(tab2_text_box, height=1, width=12)
tab2_title.grid(in_=tab2_text_box, row=0, column = 0, pady=(15,5), padx=(10,10))
tab2_title.insert(INSERT, "Dose response")
tab2_title.config(state=DISABLED, bd=0, bg = '#E5f9ff', fg='#130e07', font=('calibri', '25', 'bold'))
tab2_text_box.grid_columnconfigure(0, weight=1)
tab2_text_box.grid_rowconfigure(0, weight=1)

tab2_text = tk.Text(tab2_text_box, height=4, width=43)
tab2_text.grid(in_=tab2_text_box, row=1, column=0, sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab2_text.insert(INSERT,"Make a calibration curve and read the dose response \nfunction. For every new batch of GafChromic film\
    \nthere is a need to update the dose response. All three \nchannels (RGB) are read and calculated.")
tab2_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '13')) 
tab2_text_box.grid_columnconfigure(1, weight=1)
tab2_text_box.grid_rowconfigure(1, weight=1)

tab2_readmore_text = tk.Text(tab2_text_box, height=1, width=1)
tab2_readmore_text.grid(row=1, column=0, sticky = N+S+W+E, pady=(65,0), padx = (300,0))
tab2_readmore_text.insert(INSERT,"Read more...")
tab2_readmore_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '12', 'bold'))
tab2_text_box.grid_columnconfigure(2, weight=1)
tab2_text_box.grid_rowconfigure(2, weight=1)

tab2_box_figure = Image.open("icon_dose_response.png")
tab2_figure = ImageTk.PhotoImage(tab2_box_figure)
tab2_figure_label = Label(tab2_text_box, image=tab2_figure)
tab2_figure_label.image = tab2_figure
tab2_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab2_figure_label.config(bg='#E5f9ff')
tab2_text_box.grid_columnconfigure(3, weight=1)
tab2_text_box.grid_rowconfigure(3, weight=1)

tab3_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab3_text_box.grid(row=1, column=0, pady=(0,30), padx=(55,0))
tab3_text_box.config(bd=0, bg='#E5f9ff')

tab3_title = tk.Text(tab3_text_box, height=1, width=8)
tab3_title.grid(in_=tab3_text_box, row=0, column = 0, pady=(15,5), padx=(10,10))
tab3_title.insert(INSERT, "Map dose")
tab3_title.config(state=DISABLED, bd=0, bg = '#E5f9ff', fg='#130e07', font=('calibri', '25', 'bold'))
tab3_text_box.grid_columnconfigure(0, weight=1)
tab3_text_box.grid_rowconfigure(0, weight=1)

tab3_text = tk.Text(tab3_text_box, height=4, width=43)
tab3_text.grid(in_=tab3_text_box, row=1, column=0, sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab3_text.insert(INSERT,"Compare dose distribution in your treatment plan \nwith the measures distribution by the Gafchromic \nfilm.\
 Using the gamma evaluation index a map of \npass/fail and variations is visualised.")
tab3_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '13'))
tab3_text_box.grid_columnconfigure(1, weight=1)
tab3_text_box.grid_rowconfigure(1, weight=1)

tab3_readmore_text = tk.Text(tab3_text_box, height=1, width=1)
tab3_readmore_text.grid(row=1, column=0, sticky = N+S+W+E, pady=(65,0), padx = (285,0))
tab3_readmore_text.insert(INSERT,"Read more...")
tab3_readmore_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '12', 'bold'))
tab3_text_box.grid_columnconfigure(2, weight=1)
tab3_text_box.grid_rowconfigure(2, weight=1)

tab3_box_figure = Image.open("icon_map_dose.png")
tab3_figure = ImageTk.PhotoImage(tab3_box_figure)
tab3_figure_label = Label(tab3_text_box, image=tab3_figure)
tab3_figure_label.image = tab3_figure
tab3_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab3_figure_label.config(bg='#E5f9ff')
tab3_text_box.grid_columnconfigure(3, weight=1)
tab3_text_box.grid_rowconfigure(3, weight=1)

tab4_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab4_text_box.grid(row=1, column=1, pady=(0,30), padx=(65,0))
tab4_text_box.config(bd=0, bg='#E5f9ff')

tab4_title = tk.Text(tab4_text_box, height=1, width=7)
tab4_title.grid(in_=tab4_text_box, row=0, column = 0, pady=(15,5), padx=(10,10))
tab4_title.insert(INSERT, "Profiles")
tab4_title.config(state=DISABLED, bd=0, bg = '#E5f9ff', fg='#130e07', font=('calibri', '25', 'bold'))
tab4_text_box.grid_columnconfigure(0,weight=1)
tab4_text_box.grid_rowconfigure(0, weight=1)

tab4_text = tk.Text(tab4_text_box, height=4, width=43)
tab4_text.grid(in_=tab4_text_box, row=1, column=0, sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab4_text.insert(INSERT,"Investigate the profiles measured using GafChromic \nfilm and compare with the profiles in your treatment \nplan.\
 Using gamma evaluation an acceptance tube \ncan be places over the profile.")
tab4_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '13')) 
tab4_text_box.grid_columnconfigure(1, weight=1)
tab4_text_box.grid_rowconfigure(1, weight=1)

tab4_readmore_text = tk.Text(tab4_text_box, height=1, width=1)
tab4_readmore_text.grid(row=1, column=0, sticky = N+S+W+E, pady=(65,0), padx = (235,0))
tab4_readmore_text.insert(INSERT,"Read more...")
tab4_readmore_text.config(state=DISABLED, bd=0, bg='#E5f9ff', fg='#130E07', font=('calibri', '12', 'bold'))
tab4_text_box.grid_columnconfigure(2, weight=1)
tab4_text_box.grid_rowconfigure(2, weight=1)

tab4_box_figure = Image.open("icon_profiles.png")
tab4_figure = ImageTk.PhotoImage(tab4_box_figure)
tab4_figure_label = Label(tab4_text_box, image=tab4_figure)
tab4_figure_label.image = tab4_figure
tab4_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab4_figure_label.config(bg='#E5f9ff')
tab4_text_box.grid_columnconfigure(3, weight=1)
tab4_text_box.grid_rowconfigure(3, weight=1)

#intro_tab_canvas.configure(scrollregion = intro_tab_canvas.bbox("all"))
intro_tab_canvas.grid(row=0, column=0, sticky=N+S+W)#pack(side=LEFT, fill=BOTH)
#Globals.intro_tab.grid_columnconfigure(1, weight=2)
#Globals.intro_tab.grid_rowconfigure(1, weight=2)
#scrollbar.config(command=intro_tab_canvas.yview)

##################################### TAB 1 - CoMet ############################################


Globals.tab1_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

CoMet_explained = tk.Text(Globals.tab1_canvas, height=4, width=105)
CoMet_explained.insert(INSERT, \
"Start the correction by choosing the correct *.tif file containing the scanned image of the GafChromic film. \
The film \nshould be scanned using Epson Perfection v750 Pro with dpi setting 72 or 127. Then pick which \
folder the corrected file \nshould be uploaded to. The corrected file will be saved as a DICOM. Write filename \
and patient name (optional) before \ndoing the correction. An illustration of the corrected image will appear.")
CoMet_explained.grid(row=0, column = 0, columnspan=4, sticky=N+S+E+W, padx=(20,40), pady=(10,10))
Globals.tab1_canvas.grid_columnconfigure(0, weight=0)
Globals.tab1_canvas.grid_rowconfigure(0, weight=0)
CoMet_explained.config(state=DISABLED, bg='#ffffff', font=('calibri', '11'), relief=FLAT)

Globals.CoMet_border_1_label = Label(Globals.tab1_canvas, image = CoMet_border_dark,width=50)
Globals.CoMet_border_1_label.image=CoMet_border_dark
Globals.CoMet_border_1_label.grid(row=1, column=0, columnspan=3, sticky = W+E, padx = (0, 50), pady=(10,5))
Globals.tab1_canvas.grid_columnconfigure(1, weight=0)
Globals.tab1_canvas.grid_rowconfigure(1, weight=0)
Globals.CoMet_border_1_label.config(bg='#ffffff', borderwidth=0)

CoMet_upload_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_upload_button_frame.grid(row=1, column = 2, padx = (60, 0), pady=(10,5))
Globals.tab1_canvas.grid_columnconfigure(2, weight=0)
Globals.tab1_canvas.grid_rowconfigure(2, weight=0)
CoMet_upload_button_frame.config(bg = '#ffffff')

CoMet_upload_button = tk.Button(CoMet_upload_button_frame, text='Browse', image = Globals.upload_button_image, \
    cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=CoMet_functions.UploadAction)
CoMet_upload_button.pack(expand=True, fill=BOTH)
CoMet_upload_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
CoMet_upload_button.image = Globals.upload_button_image

Globals.CoMet_uploaded_file_text = tk.Text(Globals.CoMet_border_1_label, height=1, width=31)
Globals.CoMet_uploaded_file_text.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
Globals.CoMet_uploaded_file_text.insert(INSERT, "Upload the image you want to correct")
Globals.CoMet_uploaded_file_text.config(state=DISABLED, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')

Globals.CoMet_border_2_label = Label(Globals.tab1_canvas, image = CoMet_border_dark)
Globals.CoMet_border_2_label.image=CoMet_border_dark
Globals.CoMet_border_2_label.grid(row=2, column=0, columnspan=3, sticky=N+S+E+W, padx = (0, 50), pady=(0,15))
Globals.tab1_canvas.grid_columnconfigure(3, weight=0)
Globals.tab1_canvas.grid_rowconfigure(3, weight=0)
Globals.CoMet_border_2_label.config(bg='#ffffff', borderwidth=0)

CoMet_folder_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_folder_button_frame.grid(row=2, column = 2, padx = (60, 0), pady=(0,15))
Globals.tab1_canvas.grid_columnconfigure(4, weight=0)
Globals.tab1_canvas.grid_rowconfigure(4, weight=0)
CoMet_folder_button_frame.config(bg = '#ffffff')

CoMet_folder_button = tk.Button(CoMet_folder_button_frame, text='Browse', image = select_folder_image ,cursor='hand2',font=('calibri', '14'),\
    relief=FLAT, state=ACTIVE, command=CoMet_functions.setCoMet_export_folder)
CoMet_folder_button.pack(expand=True, fill=BOTH)
CoMet_folder_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
CoMet_folder_button.image=select_folder_image

CoMet_save_to_folder = tk.Text(Globals.CoMet_border_2_label, height=1, width=31)
CoMet_save_to_folder.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(25,0), padx=(80,0))
CoMet_save_to_folder.insert(INSERT,"Folder to save the corrected image")
CoMet_save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff') 

## Function to test the filename the user chooses for the corrected image
def testFilename():   
    Globals.CoMet_corrected_image_filename.set(Globals.CoMet_save_filename.get("1.0",'end-1c'))
    if(Globals.CoMet_corrected_image_filename.get() == " " or Globals.CoMet_corrected_image_filename.get() == "Filename"):
        Globals.CoMet_corrected_image_filename.set("Error!")
    elif(len(Globals.CoMet_corrected_image_filename.get()) >21):
        messagebox.showerror("Error", "The filename must be under 20 characters")
        Globals.CoMet_corrected_image_filename.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", (Globals.CoMet_corrected_image_filename.get()).lstrip())==None):
        messagebox.showerror("Error","Filename can only contain letters and/or numbers")
        Globals.CoMet_corrected_image_filename.set("Error!")
    else:
        Globals.CoMet_save_button_1.config(state=DISABLED)
        Globals.CoMet_save_filename.config(state=DISABLED)
        Globals.CoMet_progressbar_counter += 1
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        Globals.CoMet_progressbar_text = tk.Text(Globals.tab1_canvas, width = 5, height=1)
        Globals.CoMet_progressbar_text.grid(row=5, column=2, columnspan=1, sticky=E, padx=(0,70), pady=(40,0))
        Globals.CoMet_progressbar_text.insert(INSERT, str(Globals.CoMet_progressbar_counter*25) + "%")
        if(Globals.CoMet_progressbar_counter*25 == 100):
            Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, relief=FLAT, bg='#2C8EAD', font=('calibri', '10', 'bold'))
        else:
            Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
    

Globals.CoMet_border_3_label = Label(Globals.tab1_canvas, image = CoMet_border_dark)
Globals.CoMet_border_3_label.image=CoMet_border_dark
Globals.CoMet_border_3_label.grid(row=3, column=0, columnspan=3, sticky=N+S+E+W, padx = (0, 50), pady=(0,0))
Globals.tab1_canvas.grid_columnconfigure(5, weight=0)
Globals.tab1_canvas.grid_rowconfigure(5, weight=0)
Globals.CoMet_border_3_label.config(bg='#ffffff', borderwidth=0)

Globals.CoMet_save_button_frame_1 = tk.Frame(Globals.tab1_canvas)
Globals.CoMet_save_button_frame_1.grid(row=3, column = 2, padx = (60, 0), pady=(0,0))
Globals.tab1_canvas.grid_columnconfigure(6, weight=0)
Globals.tab1_canvas.grid_rowconfigure(6, weight=0)
Globals.CoMet_save_button_frame_1.config(bg = '#ffffff')


Globals.CoMet_save_button_1 = tk.Button(Globals.CoMet_save_button_frame_1, text='Save', image = CoMet_save_button ,cursor='hand2',font=('calibri', '14'),\
    relief=FLAT, state=ACTIVE, command=testFilename)
Globals.CoMet_save_button_1.pack(expand=True, fill=BOTH)
Globals.CoMet_save_button_1.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.CoMet_save_button_1.image = CoMet_save_button


Globals.CoMet_save_filename = tk.Text(Globals.CoMet_border_3_label, height=1, width=30)
Globals.CoMet_save_filename.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
Globals.CoMet_save_filename.insert(END,"Filename (will be saved as *.dcm)")
Globals.CoMet_save_filename.config(state=NORMAL, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')


def writeFilename(event):
    current = Globals.CoMet_save_filename.get("1.0", tk.END)
    if(current == "Filename (will be saved as *.dcm)\n"):
        Globals.CoMet_save_filename.delete("1.0", tk.END)
    else:
        Globals.CoMet_save_filename.insert("1.0", "Filename (will be saved as *.dcm)")

Globals.CoMet_save_filename.bind("<FocusIn>", writeFilename)
Globals.CoMet_save_filename.bind("<FocusOut>", writeFilename)


#Functioin to validate the patient name written in by the user
def testName():   
    Globals.CoMet_patientName.set(CoMet_save_patientName.get("1.0",'end-1c'))
    if(Globals.CoMet_patientName.get() == " " or Globals.CoMet_patientName.get() == "Patient name"):
        Globals.CoMet_patientName.set("Error!")
    elif(len(Globals.CoMet_patientName.get()) >31):
        messagebox.showerror("Error", "The Name must be under 30 characters")
        Globals.CoMet_patientName.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", (Globals.CoMet_patientName.get()).lstrip())==None):
        messagebox.showerror("Error","Name can only contain letters (not æ,ø,å) and no spaces")
        Globals.CoMet_patientName.set("Error!")
    else:
        CoMet_save_button_2.config(state=DISABLED)
        CoMet_save_patientName.config(state=DISABLED)


Globals.CoMet_border_4_label = Label(Globals.tab1_canvas, image = CoMet_border_dark)
Globals.CoMet_border_4_label.image=CoMet_border_dark
Globals.CoMet_border_4_label.grid(row=4, column=0, columnspan=3, sticky=E+W, padx = (0, 50), pady=(25,0))
Globals.tab1_canvas.grid_columnconfigure(7, weight=0)
Globals.tab1_canvas.grid_rowconfigure(7, weight=0)
Globals.CoMet_border_4_label.config(bg='#ffffff', borderwidth=0)

CoMet_save_button_frame_2 = tk.Frame(Globals.tab1_canvas)
CoMet_save_button_frame_2.grid(row=4, column = 2, padx = (60, 0), pady=(20,0))
Globals.tab1_canvas.grid_columnconfigure(8, weight=0)
Globals.tab1_canvas.grid_rowconfigure(8, weight=0)
CoMet_save_button_frame_2.config(bg = '#ffffff')

CoMet_save_button_2 = tk.Button(CoMet_save_button_frame_2, text='Save', image = CoMet_save_button ,cursor='hand2',font=('calibri', '14'),\
    relief=FLAT, state=ACTIVE, command=testName)
CoMet_save_button_2.pack(expand=True, fill=BOTH)
CoMet_save_button_2.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
CoMet_save_button_2.image = CoMet_save_button

CoMet_save_patientName = tk.Text(Globals.CoMet_border_4_label, height=1, width=30)
CoMet_save_patientName.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
CoMet_save_patientName.insert(END,"Patient name (Optional)")
CoMet_save_patientName.config(state=NORMAL, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')

def writePname(event):
    current = CoMet_save_patientName.get("1.0", tk.END)
    if(current == "Patient name (Optional)\n"):
        CoMet_save_patientName.delete("1.0", tk.END)
    else:
        CoMet_save_patientName.insert("1.0", "Patient name (Optional)")

CoMet_save_patientName.bind("<FocusIn>", writePname)
CoMet_save_patientName.bind("<FocusOut>", writePname)

CoMet_correct_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_correct_button_frame.grid(row=4, column = 4,rowspan=2, padx = (0, 0), pady=(0,0), sticky=W)
Globals.tab1_canvas.grid_columnconfigure(9, weight=0)
Globals.tab1_canvas.grid_rowconfigure(9, weight=0)
CoMet_correct_button_frame.config(bg = '#ffffff')

CoMet_correct_button = tk.Button(CoMet_correct_button_frame, text='Correct', image = CoMet_correct_button_image ,cursor='hand2',font=('calibri', '14'),\
    relief=FLAT, state=ACTIVE, command=CoMet_functions.Correct)
CoMet_correct_button.pack(expand=True, fill=BOTH)
CoMet_correct_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
CoMet_correct_button.image = CoMet_correct_button_image

Globals.CoMet_print_corrected_image = tk.Canvas(Globals.tab1_canvas , width=240, height=290)
Globals.CoMet_print_corrected_image.grid(row=0, column=4, rowspan=3, sticky=N+W+S+E, pady=(20,0))
Globals.CoMet_print_corrected_image.config(bg='#ffffff', bd = 0, relief=FLAT)
Globals.tab1_canvas.grid_columnconfigure(11,weight=0)
Globals.tab1_canvas.grid_rowconfigure(11, weight=0)
Globals.CoMet_print_corrected_image.create_image(123,148,image=CoMet_empty_image_image)
Globals.CoMet_print_corrected_image.image = CoMet_empty_image_image


def clearAll():
    #Clear out the filename
    Globals.CoMet_uploaded_file_text = tk.Text(Globals.CoMet_border_1_label, height=1, width=31)
    Globals.CoMet_uploaded_file_text.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
    Globals.CoMet_uploaded_file_text.insert(INSERT, "Upload the image you want to correct")
    Globals.CoMet_uploaded_file_text.config(state=DISABLED, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')
    Globals.CoMet_uploaded_filename.set("Error!")

    #Clear out folder
    CoMet_save_to_folder = tk.Text(Globals.CoMet_border_2_label, height=1, width=32)
    CoMet_save_to_folder.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(25,0), padx=(80,0))
    CoMet_save_to_folder.insert(INSERT,"Folder to save the corrected image")
    CoMet_save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')
    Globals.CoMet_export_folder.set("Error!")

    #Clear filename of corrected file
    Globals.CoMet_save_filename = tk.Text(Globals.CoMet_border_3_label, height=1, width=30)
    Globals.CoMet_save_filename.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
    Globals.CoMet_save_filename.insert(END,"Filename (will be saved as *.dcm)")
    Globals.CoMet_save_filename.config(state=NORMAL, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')
    Globals.CoMet_corrected_image_filename.set("Error!")
    Globals.CoMet_save_button_1.config(state=ACTIVE)

    def writeFilename(event):
        current = Globals.CoMet_save_filename.get("1.0", tk.END)
        if(current == "Filename (will be saved as *.dcm)\n"):
            Globals.CoMet_save_filename.delete("1.0", tk.END)
        else:
            Globals.CoMet_save_filename.insert("1.0", "Filename (will be saved as *.dcm)")

    Globals.CoMet_save_filename.bind("<FocusIn>", writeFilename)
    Globals.CoMet_save_filename.bind("<FocusOut>", writeFilename)

    #Clear patientname
    CoMet_save_patientName = tk.Text(Globals.CoMet_border_4_label, height=1, width=30)
    CoMet_save_patientName.grid(row=0, column=0, columnspan=3, sticky=E+W, pady=(20,20), padx=(80,0))
    CoMet_save_patientName.insert(END,"Patient name (Optional)")
    CoMet_save_patientName.config(state=NORMAL, bd=0, font=('calibri', '12'), fg='gray', bg='#ffffff')
    Globals.CoMet_patientName.set("Error!")
    CoMet_save_button_2.config(state=ACTIVE)

    def writePname(event):
        current = CoMet_save_patientName.get("1.0", tk.END)
        if(current == "Patient name (Optional)\n"):
            CoMet_save_patientName.delete("1.0", tk.END)
        else:
            CoMet_save_patientName.insert("1.0", "Patient name (Optional)")


    CoMet_save_patientName.bind("<FocusIn>", writePname)
    CoMet_save_patientName.bind("<FocusOut>", writePname)

    #Clear image
    Globals.CoMet_print_corrected_image.delete('all')
    Globals.CoMet_print_corrected_image.create_image(123,148,image=CoMet_empty_image_image)
    Globals.CoMet_print_corrected_image.image = CoMet_empty_image_image

    #Clear progressbar
    Globals.CoMet_progressbar["value"]=0
    Globals.CoMet_progressbar_counter = 0
    Globals.CoMet_progressbar_check_file = True
    Globals.CoMet_progressbar_check_folder = True
    CoMet_progressbar_text = tk.Text(Globals.tab1_canvas, height=1, width=5)
    CoMet_progressbar_text.grid(row=5, column=2, columnspan=1, sticky=E, padx=(0,70), pady=(40,0))
    CoMet_progressbar_text.insert(INSERT, "0%")
    CoMet_progressbar_text.config(state=DISABLED, bd=0, relief=FLAT, bg='#ffffff',font=('calibri', '10', 'bold'))




CoMet_clear_all_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_clear_all_button_frame.grid(row=4, column=4, rowspan=2, padx=(0,0), pady=(0,0), sticky=E)
Globals.tab1_canvas.grid_columnconfigure(13, weight=0)
Globals.tab1_canvas.grid_rowconfigure(13, weight=0)
CoMet_clear_all_button_frame.config(bg='#ffffff')

CoMet_clear_all_button = tk.Button(CoMet_clear_all_button_frame, text="Clear all", image=CoMet_clear_all_button_image, cursor='hand2', font=('calibri', '14'),\
    relief=FLAT, state=ACTIVE, command=clearAll)
CoMet_clear_all_button.pack(expand=True, fill=BOTH)
CoMet_clear_all_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
CoMet_clear_all_button.image=CoMet_clear_all_button_image

Globals.tab1_canvas.pack(expand=True, fill=BOTH)

##################################### TAB 2 - Dose response ############################################

#"To be able to perform an accurate dose caluclations using GafChromic film EBT3 \n\
#it is necessary to create a dose-respons curve for each batch of film, in addition\n\
#to a calibration scan before/along every use. The respons of GafChromic film \n\
#EBT3 is modelled using a rational function, X(D,n) = a + b/(D-c), as this has \n\
#proven to fit well with the film behavior. In the model X(D,n) is the scanner \n\
#respons in color channel n and a, b and c are constants. Because of the nature \n\
#of asymptotic fitting functions a good fit will be achieved by using doses in \n\
#geomteric progression, D, nD, nnD, etc.. Also, to avoid scanner uncertainties\n\
#each dose should be scannet three times and uploaded here where an average will be used."

#Irradiate film piece of size (Bestemt med maske?) with known doses. Place one and one\n\
#film piece in the center of the scanner and perfom three scans per dose.  "

Globals.tab2_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

dose_response_explain_text = tk.Text(Globals.tab2_canvas, height=4, width=140)
dose_response_explain_text.insert(INSERT, "\
Follow the calibration specifications given under 'Help' or 'Read more' at the first window. Upload the scanned *.tif files (there should be at least 3 of each\n\
dose level) and save. The dose response curve along with the equation will appear when enough data points are given. The uploaded files must have dpi \n\
setting 72 or 127. When saving the calibration the dose response data will be saved and can be used chosen for later use of this software. The dose response \n\
curve will be found for all three color channels, but can be removed using the check boxes. A dose response equation will only be fitted for the red channel.  " )
dose_response_explain_text.grid(row=0, column=0, columnspan=5, sticky=N+S+E+W, pady=(20,20), padx=(20,10))
Globals.tab2_canvas.grid_columnconfigure(0, weight=0)
Globals.tab2_canvas.grid_rowconfigure(0, weight=0)
dose_response_explain_text.config(state=DISABLED, font=('calibri', '11'), bg ='#ffffff', relief=FLAT)

dose_response_upload_button_frame = tk.Frame(Globals.tab2_canvas_files)
dose_response_upload_button_frame.grid(row=0, column = 0, columnspan=8, padx = (60, 0), pady=(10,5))
Globals.tab2_canvas_files.grid_columnconfigure(0, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(0, weight=0)
dose_response_upload_button_frame.config(bg = '#ffffff')

dose_response_upload_button = tk.Button(dose_response_upload_button_frame, text='Upload file', image=Globals.upload_button_image,\
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=Dose_response_functions.create_window)
dose_response_upload_button.pack(expand=True, fill=BOTH)
dose_response_upload_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
dose_response_upload_button.image = Globals.upload_button_image

check1 = Checkbutton(Globals.tab2_canvas_files, variable=Globals.dose_response_var1, command=Dose_response_functions.plot_dose_response)
check1.grid(row=1, column=1, sticky=E, padx=(30,15))
Globals.tab2_canvas_files.grid_columnconfigure(5, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(5, weight=0)
check1.config(bg='#ffffff')

check2 = Checkbutton(Globals.tab2_canvas_files, variable=Globals.dose_response_var2, command=Dose_response_functions.plot_dose_response)
check2.grid(row=1, column=3, sticky=E, padx=(45,15))
Globals.tab2_canvas_files.grid_columnconfigure(6, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(6, weight=0)
check2.config(bg='#ffffff')

check3 = Checkbutton(Globals.tab2_canvas_files, variable=Globals.dose_response_var3, command=Dose_response_functions.plot_dose_response)
check3.grid(row=1, column=5, sticky=E, padx=(35,10))
Globals.tab2_canvas_files.grid_columnconfigure(7, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(7, weight=0)
check3.config(bg='#ffffff')

red = tk.Text(Globals.tab2_canvas_files, height=1, width=4)
red.insert(INSERT, "Red")
red.grid(row=1, column=1, sticky=W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(1, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(1, weight=0)
red.config(state=DISABLED, bd=0, font=('calibri', '12'))

green = tk.Text(Globals.tab2_canvas_files, height=1, width=5)
green.insert(INSERT, "Green")
green.grid(row = 1, column = 3, sticky=W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(2, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(2, weight=0)
green.config(state=DISABLED, bd=0, font=('calibri', '12'))

blue = tk.Text(Globals.tab2_canvas_files, height=1, width=4)
blue.insert(INSERT, "Blue")
blue.grid(row=1, column=5, sticky=W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(3, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(3, weight=0)
blue.config(state=DISABLED, bd=0, font=('calibri', '12'))

dose_title = tk.Text(Globals.tab2_canvas_files, height=1, width=10)
dose_title.insert(INSERT, "Dose (cGy)")
dose_title.grid(row=1, column=0, sticky=N+S+W+E, padx=(0,15))
Globals.tab2_canvas_files.grid_columnconfigure(4, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(4, weight=0)
dose_title.config(state=DISABLED, bd=0, font=('calibri', '12'))

dose_response_save_calibration_button_frame = tk.Frame(Globals.tab2_canvas)
dose_response_save_calibration_button_frame.grid(row=2, column = 2, sticky=N+S+E+W, padx=(0,0), pady=(120,0))
Globals.tab2_canvas.grid_columnconfigure(10, weight=0)
Globals.tab2_canvas.grid_rowconfigure(10, weight=0)
dose_response_save_calibration_button_frame.config(bg = '#ffffff', height=1, width=100)
dose_response_save_calibration_button_frame.grid_propagate(0)

Globals.dose_response_save_calibration_button = tk.Button(dose_response_save_calibration_button_frame, text='Save calibration', image=dose_response_calibration_button_image, \
    cursor='hand2', font=('calibri', '12'), relief=FLAT, state=DISABLED, command=Dose_response_functions.saveCalibration)
Globals.dose_response_save_calibration_button.pack(expand=True, fill=BOTH, side=TOP)
Globals.dose_response_save_calibration_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.dose_response_save_calibration_button.image = dose_response_calibration_button_image

dose_response_clear_all_button_frame = tk.Frame(Globals.tab2_canvas)
dose_response_clear_all_button_frame.grid(row=2, column=1, sticky=N+S+E+W, padx=(0,0), pady=(120,0))
Globals.tab2_canvas.grid_columnconfigure(11, weight=0)
Globals.tab2_canvas.grid_rowconfigure(11, weight=0)
dose_response_clear_all_button_frame.config(bg='#ffffff', height=1, width=100)
dose_response_clear_all_button_frame.grid_propagate(0)

dose_response_clear_all_button = tk.Button(dose_response_clear_all_button_frame, text='Clear all', image=dose_response_clear_all_button_image, \
    cursor='hand2', font=('calibri', '12'), relief=FLAT, state=ACTIVE, command=Dose_response_functions.clear_all)
dose_response_clear_all_button.pack(expand=True, fill=BOTH, side=TOP)
dose_response_clear_all_button.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
dose_response_clear_all_button.image = dose_response_clear_all_button_image

delete_text = tk.Text(Globals.tab2_canvas_files, height=1, widt=7)
delete_text.insert(INSERT, "Delete")
delete_text.grid(row=1, column=7, sticky=N+S+E+W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(4, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(4, weight=0)
delete_text.config(state=DISABLED, bd=0, font=('calibri', '12'))

Globals.tab2_canvas.pack(expand=True, fill=BOTH)
##################################### TAB 3 - Map dose ############################################

#path = os.path.dirname(sys.argv[0])
#path= "upload.png"
#upload_button_image = ImageTk.PhotoImage(file=path)

Globals.tab3_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)


upload_film_data = tk.Button(Globals.tab3_canvas, text='Upload',image=Globals.upload_button_image, cursor='hand2', font=('calibri', '12'), \
    relief=FLAT, state=ACTIVE, width=12, command=lambda: Map_Dose.UploadAction("FILM"))
upload_film_data.place(relwidth=0.17, relheight=0.11, relx=0.3, rely=0.03)
upload_film_data.image = Globals.upload_button_image


Globals.tab3_canvas.pack(expand=True, fill=BOTH)
##################################### TAB 4 - Profiles ###########################################

Globals.tab4_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

profiles_explain_text = tk.Text(Globals.tab4_canvas, height=4, width=140)
profiles_explain_text.insert(INSERT, "\
SliceThickness i plan må være ['1','1'], ['2','2'] eller ['3','3'], Filmen må legges i xy, xz eller yz planet (lage figur?), Filmen må scannes  \n\
parallelt med retningene i skanneren (programmet vil anta dette), \n\
Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det, \n\
Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det tekst, Her kommer det, " )
profiles_explain_text.grid(row=0, column=0, columnspan=5, sticky=N+S+E+W, pady=(20,20), padx=(20,10))
Globals.tab4_canvas.grid_columnconfigure(0, weight=0)
Globals.tab4_canvas.grid_rowconfigure(0, weight=0)
profiles_explain_text.config(state=DISABLED, font=('calibri', '11'), bg ='#E5f9ff', relief=FLAT)

#profiles_upload_film_frame = tk.Frame(Globals.tab4_canvas)
#profiles_upload_film_frame.grid(row=2, column = 0, padx = (20, 0), pady=(10,0), sticky=N+S+W)
#Globals.tab4_canvas.grid_columnconfigure(1, weight=0)
#Globals.tab4_canvas.grid_rowconfigure(1, weight=0)
#profiles_upload_film_frame.config(bg = '#ffffff')

#profiles_upload_button_film = tk.Button(profiles_upload_film_frame, text='Browse', image = profiles_add_film_button_image, \
#    cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: Profile_functions.UploadAction(True))
#profiles_upload_button_film.pack(expand=True, fill=BOTH)
#profiles_upload_button_film.config(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
#profiles_upload_button_film.image = profiles_add_film_button_image

#profiles_upload_doseplan_frame = tk.Frame(Globals.tab4_canvas)
#profiles_upload_doseplan_frame.grid(row=2, column = 0, padx = (0,0), pady=(10,0), sticky=N+S+E)
#Globals.tab4_canvas.grid_columnconfigure(2, weight=0)
#Globals.tab4_canvas.grid_rowconfigure(2, weight=0)
#profiles_upload_film_frame.config(bg = '#ffffff')

#profiles_upload_button_doseplan = tk.Button(profiles_upload_doseplan_frame, text='Browse', image=profiles_add_doseplan_button_image,\
#    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda: Profile_functions.UploadAction(False))
#profiles_upload_button_doseplan.pack(expand=True, fill=BOTH)
#profiles_upload_button_doseplan.configure(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
#profiles_upload_button_doseplan.image = profiles_add_doseplan_button_image

profiles_getData_frame = tk.Frame(Globals.tab4_canvas)
profiles_getData_frame.grid(row = 3, column=0, padx = (0,0), pady=(0,0))
Globals.tab4_canvas.grid_columnconfigure(1, weight=0)
Globals.tab4_canvas.grid_rowconfigure(1, weight=0)
profiles_getData_frame.config(bg='#ffffff')

profiles_getData_button = tk.Button(profiles_getData_frame, text='Upload data', image=Globals.upload_button_image, \
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=Profile_functions.uploadData)
profiles_getData_button.pack(expand=True, fill=BOTH)
profiles_getData_button.configure(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
profiles_getData_button.image = Globals.upload_button_image

Globals.profiles_film_orientation_menu = OptionMenu(Globals.tab4_canvas, Globals.profiles_film_orientation, 'Axial', 'Coronal', 'Sagittal')
Globals.profiles_film_orientation_menu.grid(row=1, column=0, sticky=N+S, padx=(60,0))
Globals.tab4_canvas.grid_columnconfigure(2, weight=0)
Globals.tab4_canvas.grid_rowconfigure(2, weight=0)
Globals.profiles_film_orientation_menu.config(bg = '#ffffff', width=15, relief=FLAT)

film_orientation_menu_text = tk.Text(Globals.tab4_canvas, width=14, height=1)
film_orientation_menu_text.insert(INSERT, "Film orientation:")
film_orientation_menu_text.config(state=DISABLED, font=('calibri', '10'), bd = 0, relief=FLAT)
film_orientation_menu_text.grid(row=1, column=0, sticky=N+S+W, padx=(30,0), pady=(5,0))
Globals.tab4_canvas.grid_columnconfigure(3, weight=0)
Globals.tab4_canvas.grid_rowconfigure(3, weight=0)

profiles_film_orientation_help_frame = tk.Frame(Globals.tab4_canvas)
profiles_film_orientation_help_frame.grid(row=1, column=0, sticky=N+S+E, padx=(0,40))
Globals.tab4_canvas.grid_columnconfigure(6, weight=0)
Globals.tab4_canvas.grid_rowconfigure(6, weight=0)
profiles_film_orientation_help_frame.configure(bg='#ffffff')

profiles_help_button_orientation = tk.Button(profiles_film_orientation_help_frame, text='help', image=Globals.help_button, \
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=Profile_functions.help_showPlanes)
profiles_help_button_orientation.pack(expand=True, fill=BOTH)
profiles_help_button_orientation.configure(bg='#ffffff',activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
profiles_help_button_orientation.image=Globals.help_button

profiles_resetAll_frame = tk.Frame(Globals.tab4_canvas)
profiles_resetAll_frame.grid(row=10,column=0, padx=(0,0), pady=(0,0))
Globals.tab4_canvas.grid_columnconfigure(5, weight=0)
Globals.tab4_canvas.grid_rowconfigure(5, weight=0)
profiles_resetAll_frame.config(bg='#ffffff')

profiles_resetAll_button = tk.Button(profiles_resetAll_frame, text='Reset', image=dose_response_clear_all_button_image, \
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=Profile_functions.clearAll)
profiles_resetAll_button.pack(expand=True, fill=BOTH)
profiles_resetAll_button.configure(bg='#ffffff', activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
profiles_resetAll_button.image = dose_response_clear_all_button_image

film_depth_text = tk.Text(Globals.tab4_canvas, width=14, height=1)
film_depth_text.insert(INSERT, "Film depth:")
film_depth_text.config(state=DISABLED, font=('calibri', '10'), bd = 0, relief=FLAT)
film_depth_text.grid(row=2, column=0, sticky=N+S+W, padx=(30,0), pady=(5,0))
Globals.tab4_canvas.grid_columnconfigure(7, weight=0)
Globals.tab4_canvas.grid_rowconfigure(7, weight=0)

Globals.profiles_depth = tk.Text(Globals.tab4_canvas, width=7, height=1)
Globals.profiles_depth.insert(INSERT, " ")
Globals.profiles_depth.config(state=NORMAL, font=('calibri', '10'), bd=2, relief=GROOVE)
Globals.profiles_depth.grid(row=2, column=0, sticky=N+S, padx=(60,0), pady=(5,0))
Globals.tab4_canvas.grid_columnconfigure(8, weight=0)
Globals.tab4_canvas.grid_rowconfigure(8, weight=0)

profiles_depth_help_frame = tk.Frame(Globals.tab4_canvas)
profiles_depth_help_frame.grid(row=2, column=0, sticky=N+S+E, padx=(0,40))
Globals.tab4_canvas.grid_columnconfigure(9, weight=0)
Globals.tab4_canvas.grid_rowconfigure(9, weight=0)
profiles_depth_help_frame.configure(bg='#ffffff')

profiles_help_button_depth = tk.Button(profiles_depth_help_frame, text='help', image=Globals.help_button, \
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=Profile_functions.help_showDepth)
profiles_help_button_depth.pack(expand=True, fill=BOTH)
profiles_help_button_depth.configure(bg='#ffffff',activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
profiles_help_button_depth.image=Globals.help_button


Globals.tab4_canvas.pack(expand=True, fill=BOTH)
##################################### End statements ############################################
#Globals.tab_parent.place(relwidth=1, relheight=0.9, relx=0, rely=0.15)
Globals.form.mainloop()
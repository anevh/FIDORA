import tkinter as tk
from tkinter import ttk, INSERT, DISABLED, GROOVE, CURRENT, Radiobutton, NORMAL, ACTIVE, messagebox, Menu
import Globals
import re
import CoMet_functions



Globals.form.title("Master")
Globals.form.geometry("1100x600")

Globals.tab_parent.add(Globals.tab1, text='CoMet')
Globals.tab_parent.add(Globals.tab2, text='Dose-response')
Globals.tab_parent.add(Globals.tab3, text='Map dose')

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

##################################### TAB 1 - CoMet ############################################


## Text and button for uploading image 
upload_file = tk.Text(Globals.tab1, height=1, width=1)
upload_file.place(relwidth=0.28, relheight=0.05, relx=0.1, rely=0.31)
upload_file.insert(INSERT,"Upload file you want to correct:")
upload_file.config(state=DISABLED, bd=0) 
upload_box = tk.Text(Globals.tab1, height=1, width=1)
upload_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
upload_box.insert(INSERT," ")
upload_box.config(state=DISABLED, bd=0)
upload_button = tk.Button(Globals.tab1, text='Browse',cursor='hand2',font=('calibri', '14'),\
    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=CoMet_functions.UploadAction)
upload_button.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.305)


## Text and buttons for the user to choose DPI
choose_CoMet_dpi = tk.Text(Globals.tab1, height=1, width=1)
choose_CoMet_dpi.place(relwidth=0.35, relheight=0.1, relx=0.07, rely=0.41)
choose_CoMet_dpi.insert(tk.CURRENT,"Dots per inch (dpi) used during scanning: ")
choose_CoMet_dpi.config(state=DISABLED, bd=0, font=('calibri', '15'))
Radiobutton(Globals.tab1, text='72 dpi',cursor='hand2',font=('calibri', '14'), \
    variable=Globals.CoMet_dpi, value=72, command=CoMet_functions.setCoMet_dpi).place(relwidth=0.075, relheight=0.05, relx=0.13, rely=0.46)
Radiobutton(Globals.tab1, text='127 dpi',cursor='hand2',font=('calibri', '14'), \
    variable=Globals.CoMet_dpi, value=127, command=CoMet_functions.setCoMet_dpi).place(relwidth=0.077, relheight=0.05, relx= 0.23, rely=0.46)


## Text and button for the user to select folder to save corrected image
save_to_folder = tk.Text(Globals.tab1, height=1, width=1)
save_to_folder.place(relwidth=0.4, relheight=0.05, relx=0.08, rely=0.57)
save_to_folder.insert(INSERT,"Folder to save the corrected image:")
save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '15')) 
folder_box = tk.Text(Globals.tab1, height=1, width=1)
folder_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.57)
folder_box.insert(INSERT," ")
folder_box.config(state=DISABLED, bd=0, font=('calibri', '12')) 
toFolder = tk.Button(Globals.tab1, text='Browse', cursor='hand2',font=('calibri', '14'),\
   highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=CoMet_functions.setCoMet_export_folder)
toFolder.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.565)

## Function to test the filename the user chooses for the corrected image
def testFilename():   
    Globals.CoMet_corrected_image_filename.set(Globals.CoMet_corrected_image_filename_box.get("1.0",'end-1c'))
    if(Globals.CoMet_corrected_image_filename.get() == " "):
        Globals.CoMet_corrected_image_filename.set("Error!")
    elif(len(Globals.CoMet_corrected_image_filename.get()) >21):
        messagebox.showerror("Error", "The filename must be under 20 characters")
        Globals.CoMet_corrected_image_filename.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", (Globals.CoMet_corrected_image_filename.get()).lstrip())==None):
        messagebox.showerror("Error","Filename can only contain letters and/or numbers")
        Globals.CoMet_corrected_image_filename.set("Error!")
    else:
        load_corrected_image_filename.config(state=DISABLED)
        Globals.CoMet_corrected_image_filename_box.config(state=DISABLED)


## Text and box for the user to write in a filename for the corrected image, and lock it
corrected_image_filename_text = tk.Text(Globals.tab1, height=1, width=1)
corrected_image_filename_text.place(relwidt=0.4, relheight=0.05, relx=0.1, rely=0.66)
corrected_image_filename_text.insert(INSERT, "Write filename of saved image:" )
corrected_image_filename_text.config(state=DISABLED, bd=0, font=('calibri', '15'))
Globals.CoMet_corrected_image_filename_box= tk.Text(Globals.tab1, height=1, width=1)
Globals.CoMet_corrected_image_filename_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.66)
Globals.CoMet_corrected_image_filename_box.insert(INSERT, " " )
Globals.CoMet_corrected_image_filename_box.config(state=NORMAL, bd=0, font=('calibri', '12'))
load_corrected_image_filename=tk.Button(Globals.tab1, text='Save filename', cursor='hand2', font=('calibri', '14'), highlightthickness=7, \
    overrelief=GROOVE, state=ACTIVE, width=15, command=testFilename)
load_corrected_image_filename.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.65)

#Tell filetype
out_filetype_text = tk.Text(Globals.tab1, height=1, width=1)
out_filetype_text.place(relwidth=0.2, relheight=0.05, relx=0.41, rely=0.795)
out_filetype_text.insert(tk.CURRENT,"Will be saved as *.dcm")
out_filetype_text.config(state=DISABLED, bd=0, font=('calibri', '13'))

#Functioin to validate the patient name written in by the user
def testName():   
    Globals.CoMet_patientName.set(Globals.CoMet_patientName_box.get("1.0",'end-1c'))
    if(Globals.CoMet_patientName.get() == " "):
        Globals.CoMet_patientName.set("Error!")
    elif(len(Globals.CoMet_patientName.get()) >31):
        messagebox.showerror("Error", "The Name must be under 30 characters")
        Globals.CoMet_patientName.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", (Globals.CoMet_patientName.get()).lstrip())==None):
        messagebox.showerror("Error","Name can only contain letters (not æ,ø,å) and no spaces")
        Globals.CoMet_patientName.set("Error!")
    else:
        loadName.config(state=DISABLED)
        Globals.CoMet_patientName_box.config(state=DISABLED)


## Text and box for the user to write patient name
patientName_text = tk.Text(Globals.tab1, height=1, width=1)
patientName_text.place(relwidt=0.4, relheight=0.05, relx=0.12, rely=0.74)
patientName_text.insert(INSERT, "Write name of patient:" )
patientName_text.config(state=DISABLED, bd=0, font=('calibri', '15'))
Globals.CoMet_patientName_box= tk.Text(Globals.tab1, height=1, width=1)
Globals.CoMet_patientName_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.74)
Globals.CoMet_patientName_box.insert(INSERT, " " )
Globals.CoMet_patientName_box.config(state=NORMAL, bd=0, font=('calibri', '12'))
loadName=tk.Button(Globals.tab1, text='Save name', cursor='hand2', font=('calibri', '14'), highlightthickness=7, \
    overrelief=GROOVE, state=ACTIVE, width=15, command=testName)
loadName.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.725)


## Creating a button-widget to perform the correction
correct_button = tk.Button(Globals.tab1, text='Correct', cursor='hand2',font=('calibri', '18'),highlightthickness= 7,\
    overrelief=GROOVE, state=ACTIVE, width = 15, command=CoMet_functions.Correct)
correct_button.place(relwidth=0.2, relheight=0.14, relx=.18, rely=0.83)


##################################### TAB 2 - Dose response ############################################
#img_file_name="default.png"
#path_img=db_config.photo_directory + img_file_name

## Text and button for uploading image
upload_file = tk.Text(Globals.tab2, height=1, width=1)
upload_file.place(relwidth=0.28, relheight=0.05, relx=0.1, rely=0.31)
upload_file.insert(INSERT,"Upload image file for calibration:")
upload_file.config(state=DISABLED, bd=0) 
upload_box = tk.Text(Globals.tab2, height=1, width=1)
upload_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
upload_box.insert(INSERT," ")
upload_box.config(state=DISABLED, bd=0)
upload_button = tk.Button(Globals.tab2, text='Browse',cursor='hand2',font=('calibri', '14'),\
    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=CoMet_functions.UploadAction)
upload_button.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.305)

## Text and buttons for the user to choose DPI
choose_doseResponse_dpi = tk.Text(Globals.tab2, height=1, width=1)
choose_doseResponse_dpi.place(relwidth=0.35, relheight=0.5, relx=0.07, rely=0.41)
choose_doseResponse_dpi.insert(tk.CURRENT,"Dots per inch (dpi) used during scanning: ")
choose_doseResponse_dpi.config(state=DISABLED, bd=0, font=('calibri', '15'))
Radiobutton(Globals.tab2, text='72 dpi',cursor='hand2',font=('calibri', '14'), \
    variable=Globals.doseResponse_dpi, value=72, command=CoMet_functions.nothingButton).place(relwidth=0.075, relheight=0.05, relx=0.13, rely=0.46)
Radiobutton(Globals.tab2, text='127 dpi',cursor='hand2',font=('calibri', '14'), \
    variable=Globals.doseResponse_dpi, value=127, command=CoMet_functions.nothingButton).place(relwidth=0.077, relheight=0.05, relx= 0.23, rely=0.46)

#openImageTabOne=Image.open(path_img)
#imgTabOne=ImageTk.PhotoImage(openImageTabOne)
#imgLabelTabOne=tk.Label(tab2,image=imgTabOne)





##################################### TAB 3 - Map dose ############################################

temp_text = tk.Text(Globals.tab3, height=1, width=1)
temp_text.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.31)
temp_text.insert(INSERT,"lage en ny fane der en kan scanne en ukjent film og finne dose vha kalibreringskurva")
temp_text.config(state=DISABLED, bd=0) 


##################################### End statements ############################################
Globals.tab_parent.pack(expand=1, fill='both')
Globals.form.mainloop()
import tkinter as tk
from tkinter import ttk, INSERT, DISABLED, GROOVE, CURRENT, Radiobutton
import Globals


Globals.form.title("Master")
Globals.form.geometry("1100x600")

Globals.tab_parent.add(Globals.tab1, text='CoMet')
Globals.tab_parent.add(Globals.tab2, text='Dose-response')

##################################### TAB 1 - CoMet ############################################

import CoMet_functions

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
choose_CoMet_dpi.place(relwidth=0.35, relheight=0.5, relx=0.07, rely=0.41)
choose_CoMet_dpi.insert(tk.CURRENT,"Dots per inch (dpi) used during scanning: ")
choose_CoMet_dpi.config(state=DISABLED, bd=0, font=('calibri', '15'))
Radiobutton(Globals.tab1, text='72 dpi',cursor='hand2',font=('calibri', '14'), \
    variable=Globals.CoMet_dpi, value=72, command=CoMet_functions.setCoMet_dpi).place(relwidth=0.075, relheight=0.05, relx=0.13, rely=0.46)
Radiobutton(Globals.tab1, text='127 dpi',cursor='hand2',font=('calibri', '14'), \
    variable=Globals.CoMet_dpi, value=127, command=CoMet_functions.setCoMet_dpi).place(relwidth=0.077, relheight=0.05, relx= 0.23, rely=0.46)


## Text and buttons for the user to select folder to save corrected image
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

##################################### TAB 2 - Dose response ############################################

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
    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=CoMet_functions.nothingButton)
upload_button.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.305)




Globals.tab_parent.pack(expand=1, fill='both')
Globals.form.mainloop()

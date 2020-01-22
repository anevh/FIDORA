import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog
import os
from os.path import normpath, basename

def nothingButton():
    return


def UploadAction(event=None):
    Globals.CoMet_uploaded_filename.set(filedialog.askopenfilename())
    ext = os.path.splitext(Globals.CoMet_uploaded_filename.get())[-1].lower()
    if(ext==".tif"):
        uploaded_filename = tk.Text(Globals.tab1, height=1, width=1)
        uploaded_filename.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
        uploaded_filename.insert(INSERT, basename(normpath(Globals.CoMet_uploaded_filename.get()))) 
        uploaded_filename.config(state=DISABLED, bd=0, font=('calibri', '12'))
    elif(ext==""):
        Globals.CoMet_uploaded_filename.set("Error!") 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")
        Globals.CoMet_uploaded_filename.set("Error!") 

def setCoMet_dpi():
    dpi = Globals.CoMet_dpi.get()
    print(dpi)
    return dpi

def setCoMet_export_folder():
    Globals.CoMet_export_folder.set(filedialog.askdirectory())
    os.chdir(Globals.CoMet_export_folder.get())
    save_to_folder=tk.Text(Globals.tab1, height=1, width=1)
    save_to_folder.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.57)
    save_to_folder.insert(INSERT, basename(normpath(Globals.CoMet_export_folder.get())))
    save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '12'))

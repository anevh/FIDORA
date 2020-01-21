#Importing packages and functions
import tkinter as tk
from tkinter import filedialog, PhotoImage, INSERT, DISABLED, \
        NORMAL, Label, GROOVE, StringVar, Radiobutton, Menu, messagebox, FLAT, ACTIVE,END
import os
from os.path import normpath, basename
import gloVar
from GUIfunctions import *
from PIL import Image, ImageTk
    

#Setting the design of the window
gloVar.root.geometry("1000x600")
gloVar.root.config(bg='#D98880')
gloVar.root.title('CoMet')
gloVar.root.tk.call('wm', 'iconphoto', gloVar.root._w, PhotoImage(file='logo.png'))
gloVar.root.iconbitmap(default='logo.png')


#Creating the title 
fill_top = tk.Text(gloVar.root, height=3, width=1)
fill_top.place(relwidth=1, relheight=0.25, relx=0, rely=0)
fill_top.insert(INSERT," ")
fill_top.config(state=DISABLED, bd=0, font=('calibri', '40'), bg ='#FADBD8')
title_box = tk.Text(gloVar.root, height=1, width=1,fg='#CD6155')
title_box.place(relwidth=0.9, relheight=0.15, relx=0.03, rely=0)
title_box.insert(INSERT,"IMAGE CORRECTION ")
title_box.config(state=DISABLED, bd=0, font=('calibri', '40'), bg ='#FADBD8') 

#Creating subtitle
subtitle_box = tk.Text(gloVar.root, height=2, width=1)
subtitle_box.place(relwidth=0.63, relheight=0.15, relx=0.03, rely=0.1)
subtitle_box.insert(INSERT,"Image correction on scanned GafChromic film when using\
 a flat-bed scanner Epson v750 Pro ")
subtitle_box.config(state=DISABLED, bd=0, font=('calibri', '25'), bg ='#FADBD8') 

#Inserting the logo
load = Image.open("logo.png")
render = ImageTk.PhotoImage(load)
label = Label(image=render)
label.image = render
label.place(relwidt=0.19,relheight=0.13, relx=0.75, rely=0.071)
label.config(bg='#FADBD8') 

#Dividing line
fill_line = tk.Text(gloVar.root, height=1, width=1)
fill_line.place(relwidth=1, relheight=0.004, relx=0, rely=0.25)
fill_line.insert(INSERT,"  ")
fill_line.config(state=DISABLED, bd=0, font=('calibri', '40'), bg ='#17202A')

#Creating the widgets for uploading a file
upload_text = tk.Text(gloVar.root, height=1, width=1)
upload_text.place(relwidth=0.28, relheight=0.05, relx=0.1, rely=0.31)
upload_text.insert(INSERT,"Upload file you want to correct:")
upload_text.config(state=DISABLED, bd=0, font=('calibri', '15'), bg ='#D98880') 
uploaded_text = tk.Text(gloVar.root, height=1, width=1)
uploaded_text.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
uploaded_text.insert(INSERT," ")
uploaded_text.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FDFEFE') 
upload = tk.Button(gloVar.root, text='Browse',cursor='hand2',font=('calibri', '14'),\
    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=UploadAction)
upload.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.305)

#Creating the widgets where the user selects dpi (radiobuttons)
selDPI = tk.Text(gloVar.root, height=1, width=1)
selDPI.place(relwidth=0.35, relheight=0.5, relx=0.07, rely=0.41)
selDPI.insert(tk.CURRENT,"Dots per inch (dpi) used during scanning: ")
selDPI.config(state=DISABLED, bd=0, font=('calibri', '15'), bg ='#D98880') 
Radiobutton(gloVar.root, text='72 dpi',cursor='hand2',font=('calibri', '14'), bg ='#D98880', \
    variable=gloVar.DPI, value=72, command=WhatDPI).place(relwidth=0.075, relheight=0.05, relx=0.13, rely=0.46)
Radiobutton(gloVar.root, text='127 dpi',cursor='hand2',font=('calibri', '14'),bg ='#D98880', \
    variable=gloVar.DPI, value=127, command=WhatDPI).place(relwidth=0.077, relheight=0.05, relx= 0.23, rely=0.46)

#Creating widgets where the user selects correction method (radiobuttons)
selComet = tk.Text(gloVar.root, height=1, width=1)
selComet.place(relwidth=0.5, relheight=0.5, relx=0.55, rely=0.41)
selComet.insert(tk.CURRENT,"Choose which correction method to apply: ")
selComet.config(state=DISABLED, bd=0, font=('calibri', '15'), bg ='#D98880') 
Radiobutton(gloVar.root, text='Correction matrix',cursor='hand2',font=('calibri', '14'), bg ='#D98880', variable\
    =gloVar.comet, value=1,command=WhatMethod).place(relwidth=0.164, relheight=0.05, relx=0.58, rely=0.46)
Radiobutton(gloVar.root, text='Other',cursor='hand2',font=('calibri','14'),bg ='#D98880', state=DISABLED, variable\
    =gloVar.comet, value=2, command=WhatMethod).place(relwidth=0.14,relheight=0.05, relx=0.74, rely=0.46)


#Creating widgets for the user to select upload folder
folder_tx = tk.Text(gloVar.root, height=1, width=1)
folder_tx.place(relwidth=0.4, relheight=0.05, relx=0.08, rely=0.57)
folder_tx.insert(INSERT,"Folder to save the corrected image:")
folder_tx.config(state=DISABLED, bd=0, font=('calibri', '15'), bg ='#D98880') 
folder_box = tk.Text(gloVar.root, height=1, width=1)
folder_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.57)
folder_box.insert(INSERT," ")
folder_box.config(state=DISABLED, bd=0, font=('calibri', '12'), bg ='#FDFEFE') 
toFolder = tk.Button(gloVar.root, text='Browse', cursor='hand2',font=('calibri', '14'),\
    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=Export_File)
toFolder.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.565)


#Creating widgets for the user to write in a filename
selname = tk.Text(gloVar.root, height=1, width=1)
selname.place(relwidt=0.4, relheight=0.05, relx=0.1, rely=0.66)
selname.insert(INSERT, "Write filename of saved image:" )
selname.config(state=DISABLED, bd=0, font=('calibri', '15'), bg ='#D98880')
gloVar.savetofolder= tk.Text(gloVar.root, height=1, width=1)
gloVar.savetofolder.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.66)
gloVar.savetofolder.insert(INSERT, " " )
gloVar.savetofolder.config(state=NORMAL, bd=0, font=('calibri', '12'), bg ='#CCD1D1')

#Creating widgets for the user to write patient name
patientName = tk.Text(gloVar.root, height=1, width=1)
patientName.place(relwidt=0.4, relheight=0.05, relx=0.12, rely=0.74)
patientName.insert(INSERT, "Write name of patient:" )
patientName.config(state=DISABLED, bd=0, font=('calibri', '15'), bg ='#D98880')
gloVar.PatientName= tk.Text(gloVar.root, height=1, width=1)
gloVar.PatientName.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.74)
gloVar.PatientName.insert(INSERT, " " )
gloVar.PatientName.config(state=NORMAL, bd=0, font=('calibri', '12'), bg ='#CCD1D1')


#Tell filetype
outtype = tk.Text(gloVar.root, height=1, width=1)
outtype.place(relwidth=0.2, relheight=0.05, relx=0.41, rely=0.795)
outtype.insert(tk.CURRENT,"Will be saved as *.dcm")
outtype.config(state=DISABLED, bd=0, font=('calibri', '13'), bg ='#D98880') 

#Creating the menubar
menubar = Menu(gloVar.root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Restart", command=reSet)
filemenu.add_command(label="Open", command=UploadAction)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=gloVar.root.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=openHelp)
helpmenu.add_command(label="About", command=openAbout)
menubar.add_cascade(label="Help", menu=helpmenu)
gloVar.root.config(menu=menubar)


#Validate filename
def testFilename():   
    gloVar.saveTo.set(gloVar.savetofolder.get("1.0",'end-1c'))
    if(gloVar.saveTo.get() == " "):
        gloVar.saveTo.set("Error!")
    elif(len(gloVar.saveTo.get()) >21):
        messagebox.showerror("Error", "The filename must be under 20 characters")
        gloVar.saveTo.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", (gloVar.saveTo.get()).lstrip())==None):
        messagebox.showerror("Error","Filename can only contain letters and/or numbers")
        gloVar.saveTo.set("Error!")
    else:
        loadfilename.config(state=DISABLED)
        gloVar.savetofolder.config(state=DISABLED)
    
#Validate patient name
def testName():   
    gloVar.pName.set(gloVar.PatientName.get("1.0",'end-1c'))
    if(gloVar.pName.get() == " "):
        gloVar.pName.set("Error!")
    elif(len(gloVar.pName.get()) >31):
        messagebox.showerror("Error", "The Name must be under 30 characters")
        gloVar.pName.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", (gloVar.pName.get()).lstrip())==None):
        messagebox.showerror("Error","Name can only contain letters (not æ,ø,å) and no spaces")
        gloVar.pName.set("Error!")
    else:
        loadName.config(state=DISABLED)
        gloVar.PatientName.config(state=DISABLED)

# Creating button to lock the filename
loadfilename=tk.Button(gloVar.root, text='Save filename', cursor='hand2', font=('calibri', '14'), highlightthickness=7, \
    overrelief=GROOVE, state=ACTIVE, width=15, command=testFilename)
loadfilename.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.65)

#Creating button to lock the name of the patient
loadName=tk.Button(gloVar.root, text='Save name', cursor='hand2', font=('calibri', '14'), highlightthickness=7, \
    overrelief=GROOVE, state=ACTIVE, width=15, command=testName)
loadName.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.725)

#Creating a button-widget to perform the correction
correct = tk.Button(gloVar.root, text='Correct', cursor='hand2',font=('calibri', '18'),highlightthickness= 7,\
    overrelief=GROOVE, state=ACTIVE, width = 15, command=Correct)
correct.place(relwidth=0.2, relheight=0.14, relx=.18, rely=0.83)


gloVar.root.mainloop()




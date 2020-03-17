import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog,\
     PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE
import os
from PIL import Image, ImageTk

def UploadAction():
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(ext==".tif"):
        img = Image.open(file)
        if(not (img.width == 1016 or img.width == 576)):
            messagebox.showerror("Error", "Dpi in image has to be 127 or 72")
            return

        canvas = Canvas(Globals.profile_film_visual, bd=0)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)

        scale_horizontal = img.width/408
        scale_vertical = img.height/508
        img = img.resize((408,508))
        img = ImageTk.PhotoImage(image=img)
        canvas.image = img

        canvas.create_image(0,0,image=img,anchor="nw")
        canvas.config(scrollregion=canvas.bbox(ALL))

    elif(ext==""):
        return 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")
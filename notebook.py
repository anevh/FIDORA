import tkinter as tk
from tkinter import ttk, INSERT, DISABLED
import Globals


#form = tk.Tk()
Globals.form.title("Master")
Globals.form.geometry("1100x600")

#tab_parent = ttk.Notebook(form)

#tab1 = ttk.Frame(Globals.tab_parent)
#tab2 = ttk.Frame(Globals.tab_parent)

Globals.tab_parent.add(Globals.tab1, text='CoMet')
Globals.tab_parent.add(Globals.tab2, text='Dose-response')

##################################### TAB 1 - CoMet ############################################

upload_file = tk.Text(Globals.tab1, height=1, width=1)
upload_file.place(relwidth=0.28, relheight=0.05, relx=0.1, rely=0.31)
upload_file.insert(INSERT,"Upload file you want to correct:")
upload_file.config(state=DISABLED, bd=0) 
upload_box = tk.Text(Globals.tab1, height=1, width=1)
upload_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
upload_box.insert(INSERT," ")
upload_box.config(state=DISABLED, bd=0)
#upload_button = tk.Button(tab1, text='Browse',cursor='hand2',font=('calibri', '14'),\
#    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=UploadAction)
#upload_button.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.305)


##################################### TAB 2 - Dose respons ############################################





Globals.tab_parent.pack(expand=1, fill='both')
Globals.form.mainloop()

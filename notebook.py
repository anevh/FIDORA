import tkinter as tk
from tkinter import ttk, INSERT, DISABLED


form = tk.Tk()
form.title("Master")
form.geometry("1100x600")

tab_parent = ttk.Notebook(form)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)

tab_parent.add(tab1, text='CoMet')
tab_parent.add(tab2, text='Dose-response')

tab_parent.pack(expand=1, fill='both')

upload_file = tk.Text(tab1, height=1, width=1)
upload_file.place(relwidth=0.28, relheight=0.05, relx=0.1, rely=0.31)
upload_file.insert(INSERT,"Upload file you want to correct:")
upload_file.config(state=DISABLED, bd=0) 
upload_box = tk.Text(tab1, height=1, width=1)
upload_box.place(relwidth=0.3, relheight=0.05, relx=0.41, rely=0.31)
upload_box.insert(INSERT," ")
upload_box.config(state=DISABLED, bd=0)
#upload_button = tk.Button(tab1, text='Browse',cursor='hand2',font=('calibri', '14'),\
#    highlightthickness= 7,overrelief=GROOVE, state=tk.ACTIVE, width = 15, command=UploadAction)
#upload_button.place(relwidth=0.15, relheight=0.06, relx=0.75, rely=0.305)


form.mainloop()

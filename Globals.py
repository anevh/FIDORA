import tkinter as tk
from tkinter import ttk, StringVar

global form 
form = tk.Tk()

global tab_parent
tab_parent = ttk.Notebook(form)

global tab1
tab1 = ttk.Frame(tab_parent)
global tab2
tab2 = ttk.Frame(tab_parent)

global CoMet_dpi
CoMet_dpi = "127"

global doseResponse_dpi
doseResponse_dpi="127"

global CoMet_uploaded_filename 
CoMet_uploaded_filename=StringVar(tab1)
CoMet_uploaded_filename.set("Error!")

global doseResponse_uploaded_filename 
doseResponse_uploaded_filename=StringVar(tab2)
doseResponse_uploaded_filename.set("Error!")
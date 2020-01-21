import tkinter as tk
from tkinter import ttk

global form 
form = tk.Tk()

global tab_parent
tab_parent = ttk.Notebook(form)

global tab1
tab1 = ttk.Frame(tab_parent)
global tab2
tab2 = ttk.Frame(tab_parent)
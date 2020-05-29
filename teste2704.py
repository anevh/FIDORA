from tkinter import *
root = Tk()
textWidget = Text(root)

textWidget.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
string= """Step 2: Working with the scanner
        Step 3: Scanner settings
        Step 4: Scanning  
        Step 1: Before irradiation
          Before irradiation of the GafChromic EBT3 film, remember to indicate which direction is  
        landscape direction on the film. Each film or film fragment must be marked with an 
        orientation. Film should always keep the same orientation (portrait or landscape) on the 
        scanner, and in this program you must use landscape orientation. Use the marks to place films
        consistently on the scanner. """
textWidget.insert(END,string)
textWidget.config(wraplength=500)

root.geometry('600x1000')
root.mainloop()
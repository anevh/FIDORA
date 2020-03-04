import tkinter as tk
root = tk.Tk()

S1 = tk.Scrollbar(root)
template1 = tk.Text(root, height=100, width=100)
S1.pack(side=tk.RIGHT, fill=tk.Y)
template1.pack(side=tk.RIGHT, fill=tk.Y)
template1.config(yscrollcommand=S1.set)
template1.insert(tk.END, "Nummer 1")

S2 = tk.Scrollbar(root)
template2 = tk.Text(root, height=100, width=100)
S2.pack(side=tk.RIGHT, fill=tk.Y)
template2.pack(side=tk.RIGHT, fill=tk.Y)
template2.config(yscrollcommand=S2.set)
template2.insert(tk.END, "nummer 2")

S3 = tk.Scrollbar(root)
template3 = tk.Text(root, height=100, width=100)
S3.pack(side=tk.RIGHT, fill=tk.Y)
template3.pack(side=tk.RIGHT, fill=tk.Y)
template3.config(xscrollcommand=S3.set)
template3.insert(tk.END, "nummer 3")

tk.mainloop()
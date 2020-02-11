########################## En fil kun for testing av syntax etc ########################

"""
a = "HEI"

print(type(a))

a = "3"

try:
    a = float(a)
    print(a)
    print(type(a))
except:
    print("did not work")

"""

A = [[2, 6], [31, 3], [1,9]]
print(A)
A = sorted(A,key=lambda l:l[0])
print(A)

del A[0]
print(A)
"""
A.append([3,2])
print(A[0][:])

print(A)
if 2 in A[1]:
    print("Ja")
if not [3,4] in A:
    print("Nei")


list1 = [item[0] for item in A]
print(list1)


list2 = [3,6,1,8,3]
print(list2)
list3 = sorted(list2)
print(list2)
print(list3)

"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [100, 100] },}})

style.theme_use("MyStyle")

a_notebook = ttk.Notebook(root, width=200, height=200)
a_tab = ttk.Frame(a_notebook)
a_notebook.add(a_tab, text = 'This is the first tab')
another_tab = ttk.Frame(a_notebook)
a_notebook.add(another_tab, text = 'This is another tab')
a_notebook.pack(expand=True, fill=tk.BOTH)
root.configure(bg='#D68910')
tk.Button(root, text='Some Text!').pack(fill=tk.X)

root.mainloop()
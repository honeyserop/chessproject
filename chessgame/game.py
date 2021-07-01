import sqlite3
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

    global set_name
    set_name = ""
    def changeText():
        label.configure(text=set_name)
    root = Tk()

    label = Label(root, text="Text")
    entry = Entry(root, text="Enter set name", textvariable=set_name).pack()
    button = Button(root,text="Click to change text below", command=lambda:changeText())
    button.pack()
    label.pack()
    root.mainloop()



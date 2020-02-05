import tkinter as tk
from Application import *
from tkinter import messagebox


def callback():
    if messagebox.askokcancel('Quit', 'Do you really wish to quit?'):
        root.destroy()

root = tk.Tk()
root.title('Daliy Report Automation Ver 0.1 by Yooseok Seo')
root.protocol('WM_DELETE_WINDOW', callback)
app = Application(master=root)
app.mainloop()
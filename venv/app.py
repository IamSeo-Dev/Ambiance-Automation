import tkinter as tk
from Application import *
from tkinter import messagebox
from datetime import date


def save_and_quit():
    if messagebox.askokcancel('Quit', 'Do you really wish to quit?'):
        daily_report = app.get_daily_report()
        todo_list = app.get_todo_list()

        with open(f'Daily Report({date.today().strftime("%m%d%y")}).txt', 'w') as f:
            f.write(daily_report)

        with open('TODO List.txt', 'w') as f:
            f.write(todo_list)

        root.destroy()


root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', save_and_quit)
root.title('Daliy Report Automation Ver 0.1 by Yooseok Seo')
app = Application(master=root)
app.mainloop()
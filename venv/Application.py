import tkinter as tk
from datetime import date
from email_sender import send_email
from tkinter import messagebox
import os.path


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.load_auto_saved_file()

        # initialize local value

        # date value for email Subject and email Body content
        # TODO LIST!
        # Currently, this value cannot be update automatically
        self.today = date.today().strftime("%m/%d/%y")

    def load_auto_saved_file(self):
        # it will check auto saved file exists or not
        # if not, it will create a new file for saving
        if not os.path.isfile(f'Daily Report({date.today().strftime("%m%d%y")}).txt'):
            open(f'Daily Report({date.today().strftime("%m%d%y")}).txt', 'w')

        if not os.path.isfile('TODO List.txt'):
            open('TODO List.txt', 'w')

        with open(f'Daily Report({date.today().strftime("%m%d%y")}).txt', 'r', encoding='utf-8') as f:
            self.daily_report_text.insert(1.0, f.read())
        with open('TODO List.txt', 'r', encoding='utf-8') as f:
            self.todo_list_text.insert(1.0, f.read())

    def create_widgets(self):
        self.master.title('Daliy Report Automation Ver 0.3 by Yooseok Seo')
        self.master.protocol('WM_DELETE_WINDOW', self.save_and_quit)
        # Frames
        self.main_menu_frame = tk.Frame(self.master).grid(row=0)
        self.content_frame = tk.Frame(self.master).grid(row=1)
        self.status_frame = tk.Frame(self.master).grid(row=2)

        # Sub Frames
        self.daily_frame = tk.Frame(self.content_frame).grid(row=0)
        self.todo_frame = tk.Frame(self.content_frame).grid(row=1)
        self.btn_frame = tk.Frame(self.content_frame).grid(row=2)

        # Main Menu Frame
        #self.menu = tk.Menu(self.master)
        #self.master.config(menu=menu)

        # create the file object
        #file = tk.Menu(self.menu)
        #file.add_command(label='Quit', command=self.save_and_quit)
        # TODO!

        # Content Frame - Daily
        self.daily_report_title_label = tk.Label(self.daily_frame, text='Daily Report')
        self.daily_report_title_label.grid(row=0, sticky='w', columnspan=2)
        self.daily_report_text = tk.Text(self.daily_frame)
        self.daily_report_text.grid(row=1, columnspan=2)

        # Content Frame - Todo
        self.todo_list_title_label = tk.Label(self.todo_frame, text='Todo List')
        self.todo_list_title_label.grid(row=2, sticky='w', columnspan=2)
        self.todo_list_text = tk.Text(self.todo_frame)
        self.todo_list_text.grid(row=3, columnspan=2)

        # Content Frame - Btn
        self.send_btn = tk.Button(self.btn_frame, text='Send', command=self.send_daily_report)
        self.send_btn.grid(row=4, column=0, sticky='we')
        self.save_btn = tk.Button(self.btn_frame, text='Save', command=self.save)
        self.save_btn.grid(row=4, column=1, sticky='we')
        # Status Frame
        # TODO!

    def get_daily_report(self):
        return self.daily_report_text.get('1.0', 'end-1c')

    def get_todo_list(self):
        return self.todo_list_text.get('1.0', 'end-1c')

    def send_daily_report(self):
        (daily_text, todo_text) = self.retrieve_inputs()
        body_text = daily_text + todo_text
        send_email(body_text)

    def retrieve_inputs(self):
        daily_report_title_text = f'Daily Report ({self.today})\n'
        daily_report_text = daily_report_title_text + self.get_daily_report() + '\n'
        todo_list_title_text = f'TODO List\n'
        todo_list_text = todo_list_title_text + self.get_todo_list() + '\n'
        return daily_report_text, todo_list_text

    def save_and_quit(self):
        if messagebox.askokcancel('Quit', 'Do you really wish to quit?'):
            self.save()
            self.master.destroy()

    def save(self):
        daily_report = self.get_daily_report()
        todo_list = self.get_todo_list()

        with open(f'Daily Report({date.today().strftime("%m%d%y")}).txt', 'w', encoding='utf-8') as f:
            f.write(daily_report)

        with open('TODO List.txt', 'w', encoding='utf-8') as f:
            f.write(todo_list)

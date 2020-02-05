import tkinter as tk
from datetime import date
from email_sender import send_email


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

        # initalize local value

        # date value for email Subject and email Body content
        # TODO LIST!
        # Currently, this value cannot be update automatically
        self.today = date.today().strftime("%m/%d/%y")

    def create_widgets(self):
        # Frames
        self.main_menu_frame = tk.Frame(self.master).grid(row=0)
        self.content_frame = tk.Frame(self.master).grid(row=1)
        self.status_frame = tk.Frame(self.master).grid(row=2)

        # Sub Frames
        self.daily_frame = tk.Frame(self.content_frame).grid(row=0)
        self.todo_frame = tk.Frame(self.content_frame).grid(row=1)
        self.btn_frame = tk.Frame(self.content_frame).grid(row=2)

        # Main Menu Frame
        # TODO!

        # Content Frame - Daily
        self.daily_report_title_label = tk.Label(self.daily_frame, text='Daily Report')
        self.daily_report_title_label.grid(row=0, sticky='w')
        self.daily_report_text = tk.Text(self.daily_frame)
        self.daily_report_text.grid(row=1)

        # Content Frame - Todo
        self.todo_list_title_label = tk.Label(self.todo_frame, text='Todo List')
        self.todo_list_title_label.grid(row=2, sticky='w')
        self.todo_list_text = tk.Text(self.todo_frame)
        self.todo_list_text.grid(row=3)

        # Content Frame - Btn
        self.send_btn = tk.Button(self.btn_frame, text='Send', command=self.send_daily_report)
        self.send_btn.grid(row=4, sticky='nsew')

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

        # TODO!
        # Send Email Function Call Here

    def retrieve_inputs(self):
        daily_report_title_text = f'Daily Report ({self.today})\n'
        daily_report_text = daily_report_title_text + self.get_daily_report() + '\n'
        todo_list_title_text = f'TODO List\n'
        todo_list_text = todo_list_title_text + self.get_todo_list() + '\n'
        return (daily_report_text, todo_list_text)

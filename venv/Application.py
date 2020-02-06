import tkinter as tk
from datetime import date
from tkinter import messagebox
import os.path
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
import threading
import time


def convert_to_html(body):
    html_start_body_tag = '<html><head><style>p { font-size: 22px; font-family: Arial} div{font-size: 16px; ' \
                          'font-family: Arial}</style></head><body>'
    html_end_body_tag = '</body></html>'
    html_body_content = ''

    for line in body.splitlines():
        if "Daily Report" in line:
            html_body_content += '<p>' + line + '</p>'
        elif "TODO" in line:
            html_body_content += '<br><p>' + line + '</p>'
        else:
            html_body_content += '<div>' + line + '</div>'

    return html_start_body_tag + html_body_content + html_end_body_tag


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # initialize local value

        # TODO LIST!
        # Currently, this value cannot be update automatically
        self.today = date.today().strftime("%m/%d/%y")
        self.update_current_time()
        self.master = master
        self.grid()

        self.create_widgets()
        self.load_auto_saved_file()
        self.auto_save()

    def do_nothing(self):
        print('nothing')

    def update_current_time(self):
        self.named_tuple = time.localtime()  # get struct_time
        self.time_string = time.strftime('at %H:%M:%S on %m/%d/%Y', self.named_tuple)


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
        self.master.title('Daliy Report Automation Ver 0.4 by Yooseok Seo')
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
        self.menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label='New...', command=self.do_nothing)
        file_menu.add_command(label='Open...', command=self.do_nothing)
        file_menu.add_command(label='Save...', command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label='Settings', command=self.do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.save_and_quit)
        self.menu_bar.add_cascade(label='File', menu=file_menu)
        self.master.config(menu=self.menu_bar)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label='About Daily Report', command=self.do_nothing)
        self.menu_bar.add_cascade(label='Help', menu=help_menu)


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
        self.status_bar = tk.Label(self.status_frame, text='Hello World', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=5, columnspan=2, sticky='wesn')

    def get_daily_report(self):
        return self.daily_report_text.get('1.0', 'end-1c')

    def get_todo_list(self):
        return self.todo_list_text.get('1.0', 'end-1c')

    def send_daily_report(self):
        (daily_text, todo_text) = self.retrieve_inputs()
        body_text = daily_text + todo_text
        # threading
        #saver = threading.Thread(target= self.send_email(body_text))
        self.send_email(body_text)
        #saver.start()

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
        self.status_bar_update('Contents are saving now...')

        with open(f'Daily Report({date.today().strftime("%m%d%y")}).txt', 'w', encoding='utf-8') as f:
            f.write(daily_report)

        with open('TODO List.txt', 'w', encoding='utf-8') as f:
            f.write(todo_list)
        self.status_bar_update(f'Contents are saved successfully {self.time_string}')

    def auto_save(self):
        self.save()
        self.status_bar_update(f'Auto Saved {self.time_string}')
        self.master.after(60000 * config.system_settings['auto_save_time_interval_min'], self.auto_save)

    def status_bar_update(self, text):
        self.update_current_time()
        self.status_bar['text'] = text

    def send_email(self, body):
        # test value only
        # sender_email = 'yooseokseo@ambianceapparel.com'
        # receiver_email = 'yooseokseo@ambianceapparel.com'
        sender_email = config.email_account_settings['username']
        receiver_email = config.daily_report_settings['recipient']
        password = config.email_account_settings['password']

        message = MIMEMultipart('alternative')
        message["Subject"] = f'Daily Report ({date.today().strftime("%m/%d/%y")})'
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the HTML version of your message
        html = convert_to_html(body)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(config.email_account_settings['outgoing_mail_server'],
                              config.email_account_settings['server_port_number_SSL'],
                              context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        self.status_bar_update(f'Daily Report was sent successfully {self.time_string}')





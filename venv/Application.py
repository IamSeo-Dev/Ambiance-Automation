import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import date
import os.path
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
import time
from font import *


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
        elif "" == line:
            html_body_content += '<br>'
        elif "-" in line:
            html_body_content += '<div>&nbsp&nbsp&nbsp&nbsp&nbsp' + line + '</div>'
        else:
            html_body_content += '<div>' + line + '</div>'

    return html_start_body_tag + html_body_content + html_end_body_tag


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # initialize local value
        self.daily_report_path = 'Daily\\'
        self.todo_list_path = 'Todo\\'
        # TODO LIST!
        # Currently, this value cannot be update automatically
        self.today = date.today().strftime("%m/%d/%y")
        self.update_current_time()
        self.master = master
        self.grid()
        self.create_styles()
        self.create_widgets()
        self.load_auto_saved_file()
        self.auto_save()

    def do_nothing(self):
        print('nothing')

    def create_settings_widgets(self):
        settings = tk.Toplevel()
        settings.title('Settings')
        settings.geometry('420x600')

        settings_tab_control = ttk.Notebook(settings)
        btn_frame = ttk.Frame(settings, height=30)
        btn_frame.pack(side='bottom', fill='x')
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        general_settings_frame = ttk.Frame(settings_tab_control)
        email_settings_frame = ttk.Frame(settings_tab_control)
        daily_settings_frame = ttk.Frame(settings_tab_control)
        weekly_settings_frame = ttk.Frame(settings_tab_control)
        backup_frame = ttk.Frame(settings_tab_control)
        todo_frame = ttk.Frame(settings_tab_control)

        settings_tab_control.add(general_settings_frame, text='General')
        settings_tab_control.add(email_settings_frame, text=' Email ')
        settings_tab_control.add(daily_settings_frame, text='  Daily  ')
        settings_tab_control.add(todo_frame, text='  Todo  ')
        settings_tab_control.add(weekly_settings_frame, text='Weekly')
        settings_tab_control.add(backup_frame, text='Backup')


        settings_tab_control.pack(fill='both', expand=True)

        email_title_1 = ttk.Label(email_settings_frame, text='Server Information', font=TITLE)
        email_title_1.grid(row=0, sticky='W', padx=(5, 1), pady=(10, 1))
        email_content_1_1 = ttk.Label(email_settings_frame, text='Outgoing Mail Server(SMTP) : ', font=CONTENT)
        email_content_1_1.grid(row=1, sticky='W', padx=(10, 2))
        email_content_1_2 = ttk.Label(email_settings_frame, text='Server Port Number(SSL) : ', font=CONTENT)
        email_content_1_2.grid(row=2, sticky='W', padx=(10, 2))

        email_title_2 = ttk.Label(email_settings_frame, text='Logon Information', font=TITLE)
        email_title_2.grid(row=3, sticky='W', padx=(5, 1), pady=(10, 1))
        email_content_2_1 = ttk.Label(email_settings_frame, text='UserName : ', font=CONTENT)
        email_content_2_1.grid(row=4, sticky='W', padx=(10, 2))
        email_content_2_2 = ttk.Label(email_settings_frame, text='Password : ', font=CONTENT)
        email_content_2_2.grid(row=5, sticky='W', padx=(10, 2))

        email_entry1 = ttk.Entry(email_settings_frame, justify='center', width=40)
        email_entry1.grid(row=1, column=1)
        email_entry1.insert(0, config.email_account_settings['outgoing_mail_server'])
        email_entry2 = ttk.Entry(email_settings_frame, justify='center', width=40)
        email_entry2.grid(row=2, column=1)
        email_entry2.insert(0, config.email_account_settings['server_port_number_SSL'])
        email_entry3 = ttk.Entry(email_settings_frame, justify='center', width=40)
        email_entry3.grid(row=4, column=1)
        email_entry3.insert(0, config.email_account_settings['username'])
        email_entry4 = ttk.Entry(email_settings_frame, justify='center', width=40, show='*')
        email_entry4.grid(row=5, column=1)
        email_entry4.insert(0, config.email_account_settings['password'])
        test_btn = tk.Button(email_settings_frame, text='Send Test Email', font=BUTTON)
        test_btn.grid(row=6, column=1, pady=(10, 1))


        btn1 = tk.Button(btn_frame, text='OK', font=BUTTON)
        btn1.grid(row=0, column=0, sticky='we')
        btn2 = tk.Button(btn_frame, text='Cancel', font=BUTTON)
        btn2.grid(row=0, column=1, sticky='we')



        settings.mainloop()


    def update_today_date(self):
        self.today = date.today().strftime("%m/%d/%y")

    def update_current_time(self):
        self.stime = time.localtime()  # get struct_time
        self.time_string = time.strftime('at %H:%M:%S on %m/%d/%Y', self.stime)

    def load_auto_saved_file(self):
        # it will check auto saved file exists or not
        # if not, it will create a new file for saving

        if not os.path.isfile(f'{self.daily_report_path}Daily Report({date.today().strftime("%m%d%y")}).txt'):
            open(f'{self.daily_report_path}Daily Report({date.today().strftime("%m%d%y")}).txt', 'w')

        if not os.path.isfile(f'{self.todo_list_path}TODO List.txt'):
            open(f'{selg.todo_list_path}TODO List.txt', 'w')

        with open(f'{self.daily_report_path}Daily Report({date.today().strftime("%m%d%y")}).txt', 'r', encoding='utf-8') as f:
            self.daily_report_text.insert(1.0, f.read())
        with open(f'{self.todo_list_path}TODO List.txt', 'r', encoding='utf-8') as f:
            self.todo_list_text.insert(1.0, f.read())

    def create_styles(self):
        style = ttk.Style()
        style.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {"configure": {"padding": [5, 5]}, }})

        style.theme_use("MyStyle")

    def create_widgets(self):
        self.master.title('Ambiance Task Automation Ver 0.5 by Yooseok Seo')
        self.master.protocol('WM_DELETE_WINDOW', self.save_and_quit)

        # Main Menu Frame
        self.main_menu_frame = tk.Frame(self.master).grid(row=0)
        self.menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label='New...', command=self.do_nothing)
        file_menu.add_command(label='Open...', command=self.do_nothing)
        file_menu.add_command(label='Save...', command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label='Settings', command=lambda: self.create_settings_widgets())
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.save_and_quit)
        self.menu_bar.add_cascade(label='File', menu=file_menu)
        self.master.config(menu=self.menu_bar)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label='About Daily Report', command=self.do_nothing)
        self.menu_bar.add_cascade(label='Help', menu=help_menu)

        # Tab Menu

        self.tab_control = ttk.Notebook(self.master)
        self.tab_control.grid(row=1, sticky='wens')
        self.daily_frame = ttk.Frame(self.tab_control)
        self.weekly_frame = ttk.Frame(self.tab_control)
        self.backup_frame = ttk.Frame(self.tab_control)

        # Notebook (Tab Frames)

        self.daily_icon = tk.PhotoImage(file=r'icon\daily_r.png')
        self.weekly_icon = tk.PhotoImage(file=r'icon\weekly_r.png')
        self.backup_icon = tk.PhotoImage(file=r'icon\backup.png')
        self.tab_control.add(self.daily_frame, text='  Daily  ', image=self.daily_icon, compound='top')
        self.tab_control.add(self.weekly_frame, text='Weekly', image=self.weekly_icon, compound='top')
        self.tab_control.add(self.backup_frame, text='Backup', image=self.backup_icon, compound='top')

        # Content Frame - Daily
        self.daily_report_title_label = ttk.Label(self.daily_frame, text='Daily Report', font=TITLE)
        self.daily_report_title_label.grid(row=2, sticky='w', columnspan=2)
        self.daily_report_text = tk.Text(self.daily_frame)
        self.daily_report_text.grid(row=3, columnspan=2)

        # Content Frame - Todo
        self.todo_list_title_label = ttk.Label(self.daily_frame, text='Todo List', font=TITLE)
        self.todo_list_title_label.grid(row=4, sticky='w', columnspan=2)
        self.todo_list_text = tk.Text(self.daily_frame)
        self.todo_list_text.grid(row=5, columnspan=2)

        # Content Frame - Btn
        self.send_btn = tk.Button(self.daily_frame, text='Send', command=self.send_daily_report, font=BUTTON)
        self.send_btn.grid(row=6, column=0, sticky='we')
        self.save_btn = tk.Button(self.daily_frame, text='Save', command=self.save, font=BUTTON)
        self.save_btn.grid(row=6, column=1, sticky='we')

        # Status Frame
        self.status_frame = tk.Frame(self.master).grid(row=7)

        self.status_bar = tk.Label(self.status_frame, text='Ready', relief='sunken', anchor='w')
        self.status_bar.grid(row=7, columnspan=2, sticky='wesn')

    def get_daily_report(self):
        return self.daily_report_text.get('1.0', 'end-1c')

    def get_todo_list(self):
        return self.todo_list_text.get('1.0', 'end-1c')

    def send_daily_report(self):
        (daily_text, todo_text) = self.retrieve_inputs()
        body_text = daily_text + todo_text
        # threading
        # saver = threading.Thread(target= self.send_email(body_text))
        self.send_email(body_text)
        # saver.start()

    def retrieve_inputs(self):
        daily_report_title_text = f'Daily Report ({self.today})\n'
        daily_report_text = daily_report_title_text + self.get_daily_report() + '\n'
        todo_list_title_text = f'TODO List\n'
        todo_list_text = todo_list_title_text + self.get_todo_list() + '\n'
        return daily_report_text, todo_list_text

    def save_and_quit(self):
        if messagebox.askokcancel('Quit', 'Do You Really Wish To Quit?'):
            self.save()
            self.master.destroy()

    def save(self):
        daily_report = self.get_daily_report()
        todo_list = self.get_todo_list()
        self.status_bar_update('Contents are saving now...')

        with open(f'{self.daily_report_path}Daily Report({date.today().strftime("%m%d%y")}).txt', 'w', encoding='utf-8') as f:
            f.write(daily_report)

        with open(f'{self.todo_list_path}TODO List.txt', 'w', encoding='utf-8') as f:
            f.write(todo_list)
        self.status_bar_update(f'Contents are saved successfully {self.time_string}')

    def auto_save(self):
        self.save()
        self.update_today_date()
        self.status_bar_update(f'Auto Saved {self.time_string}')
        self.master.after(60000 * config.general_settings['auto_save_time_interval_min'], self.auto_save)

    def status_bar_update(self, text):
        self.update_current_time()
        self.status_bar['text'] = text

    def send_email(self, body):
        sender_email = config.email_account_settings['username']
        receiver_email = config.daily_report_settings['recipient']
        password = config.email_account_settings['password']

        message = MIMEMultipart('alternative')
        message["Subject"] = f'Daily Report ({date.today().strftime("%m/%d/%y")})'
        message["From"] = sender_email
        message["To"] = receiver_email

        print(body)

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

        self.status_bar_update(
            f'Daily Report was sent to [{config.daily_report_settings["recipient"]}] successfully {self.time_string}')

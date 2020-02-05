import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
#import config


def send_email(body):
    # test value only
    sender_email = 'yooseokseo@ambianceapparel.com'
    receiver_email = 'yooseokseo@ambianceapparel.com'
    #sender_email = config.email_account_settings['username']
    #receiver_email = config.daily_report_settings['recipient']
    #password = config.email_account_settings['password']

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

    #with smtplib.SMTP_SSL(config.email_account_settings['outgoing_mail_server'],
    #                      config.email_account_settings['server_port_number_SSL'],
    #                      context=context) as server:
    #    server.login(sender_email, password)
    #    server.sendmail(
    #        sender_email, receiver_email, message.as_string()
    #    )
    print(message.as_string())

def convert_to_html(body):
    html_start_body_tag = '<html><body>'
    html_end_body_tag = '</body></html>'
    html_body_content = ''

    for line in body.splitlines():
        if "Daily Report" in line :
            html_body_content += '<p style="font-size: 15px">' + line + '</p>'
        elif "TODO" in line :
            html_body_content += '<br><p style="font-size: 15px">' + line + '</p>'
        else :
            html_body_content += '<div style="font-size: 13px">' + line + '</div>'
    print(html_start_body_tag + html_body_content + html_end_body_tag)
    return html_start_body_tag + html_body_content + html_end_body_tag

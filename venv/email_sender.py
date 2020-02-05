from datetime import date

def prepare_message(daily_text, todo_text):
    daily_title = f'Daily Report ({date.today().strftime("%m/%d/%y")})\n'
    todo_title = '\nTODO List\n'
    message = daily_title + daily_text + todo_title + todo_text
    print(message)

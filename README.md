Author : Yooseok Seo
Project Start Date : 2/2/2020

Main Goal
- this application will send email for daily report
  when a user clicks "send" button in the application.(ver.0.1)

- this application will save data as a file when it is closed
  and will load data from a file that is recently saved when it is opened.(ver.0.2)

- this application will save data as a file when a user clicks "Save" button. (ver.0.3)

- this application will display its status when a user asks to do something such as saving,sending reports. (ver.0.4)

- this application will have menu bar in the top of the application. (ver.0.5)

- this application will save/edit its current settings (ver.0.6)

Fixed
- UnicodeEncodeError: 'ascii' codec can't encode character '\u2013' in position 136: ordinal not in range(128)
    * Decide to use 'email' library to handel unicode Error
- No file (Auto-saved file) exist Error:
    * it will check whether saved file exists or not, if not it will create a new file.
- Application.self.today(Date) value update issue:
    * the value will be update when the app did auto-saving.

Issue
- Currently this application cannot save its settings information.

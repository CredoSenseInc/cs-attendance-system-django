from dashboard.views import create_daily_log
# your imports, e.g. Django models
import datetime
from post_office import mail
from employee.models import *
from settings.models import *
from attendance.models import *
from datetime import date
from django.template.loader import render_to_string

# Cronjob for the schedule tasks
def my_scheduled_job():
    print("Daily Log Create Task")
    create_daily_log() # Create the daily log list. Runs at 12 AM at everyday to create the table.

# Sending Emails. This task is run at specific times. 
def send_mails():
    send_summary_mail() # Summary of the day if any flags are triggered.
    send_late_email() # Sending late email at 10 AM daily.

# Summary Mail
def send_summary_mail():
    if datetime.datetime.now().time() > datetime.time(19,58,00): # as the email task is run every 5 min so we are checking if the time is 8 PM or not. We send after 8PM
        print("Sending Summary Mail")
        todays_date = date.today()
        log = attendanceLog.objects.filter(date = todays_date) # Attendance Log  of today
        settings = settings_db.objects.last() # settings mail
        for i in log:
            count = 0
            print((i.emp.emp_name))
            print(type(i.emp_in_time))
            print(type(i.emp_out_time))
            try:
                # Checking different criteria of send emails
                message = "Hey " + i.emp.emp_name + ",<br><br>"
                try:
                    if i.emp_present and i.emp_in_time >  settings.delayTime:
                        message += "- You were late (In Time: " + str(i.emp_in_time) + ")<br>"
                        count += 1
                except Exception as e:
                    print(e)
                
                try:
                    if i.emp_present and i.emp_out_time < settings.endTime:
                        message += "- You left early (Out Time: " + str(i.emp_out_time) + ")<br>"
                        count += 1
                except Exception as e:
                    print(e)

                try:
                    if i.emp_present and i.emp_out_time is None:
                        message += "- You forgot to sign out<br>"
                        count += 1
                except Exception as e:
                    print(e)

                if not i.emp_present:
                    message += " - You were absent today. If you are on leave then please ignore this email.<br>"
                    count += 1
            
                message += "<br>If there is a mistake please contact HR for Support.<br><br>Thanks,<br>CredoSense Bot."
                msg_html = render_to_string('email_summary.html', {'message': message, 'todays_date' : todays_date})
                # Checking count to check if the flags have been raised or not. If count more than 0 means we have to send mail for that person.
                if count > 0 :
                    mail.send(
                    [str(i.emp.email)], # List of email addresses also accepted
                    'CredoSense Bot <credobot@cloud.credosense.com>',
                    subject= f"Your attendance summary for {todays_date} | CredoSense",
                    html_message = msg_html
                    # html_message='Hi <strong>there</strong>!',
                )
            except Exception as e:
                print(e)


# If the user is late we send late emails
def send_late_email():
    if datetime.datetime.now().time() < datetime.time(10,58,00): # Current time less than 11 AM
        print("Sending Late Email")
        todays_date = date.today()
        log = attendanceLog.objects.filter(date = todays_date, emp_present = False) 
        for i in log:
            try:
                print(i.emp.email)
                print(i.emp.emp_name)
                emp_name = i.emp.emp_name
                message = f"Hi {emp_name},<br><br>You haven't scanned your fingerprint yet. Please sign in or else you will be absent for the day. If you are on leave then please ignore this email. If there is a mistake please contact HR for Support.<br><br>With Regards,<br>CredoSense Bot."
                msg_html = render_to_string('email_notification.html', {'message': message})
                mail.send(
                    [str(i.emp.email)], # List of email addresses also accepted
                    'CredoSense Bot <credobot@cloud.credosense.com>',
                    subject= "Please Punch In! | CredoSense",
                    html_message= msg_html,
                )
            except:
                pass
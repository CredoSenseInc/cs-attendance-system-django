from dashboard.views import create_daily_log
# your imports, e.g. Django models
import datetime
from post_office import mail
from employee.models import *
from settings.models import *
from attendance.models import *
from datetime import date
from django.template.loader import render_to_string

def my_scheduled_job():
    print("Daily Log Create Task")
    create_daily_log()

def send_mails():
    send_summary_mail()
    send_late_email()

def send_summary_mail():
    if datetime.datetime.now().time() > datetime.time(19,58,00):
        print("Sending Summary Mail")
        todays_date = date.today()
        log = attendanceLog.objects.filter(date = todays_date)
        settings = settings_db.objects.last()
        for i in log:
            count = 0
            print((i.emp.emp_name))
            print(type(i.emp_in_time))
            print(type(i.emp_out_time))
            try:
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



def send_late_email():
    if datetime.datetime.now().time() < datetime.time(10,58,00):
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
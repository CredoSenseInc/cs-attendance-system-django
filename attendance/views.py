from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from attendance.models import attendanceLog
from datetime import date
import datetime
from django.contrib import messages
import csv

# Create your views here.
@login_required(login_url='user/login/')
def update_attendance(request):
    if request.method == "POST":
        print(request.POST)
        log = attendanceLog.objects.get(id=request.POST['id'])
        try:
            if(request.POST['statusRadio']) == "1":
                log.emp_present = True
            elif(request.POST['statusRadio']) == "0":
                log.emp_present = False
        except:
            pass

        try:
            log.date = request.POST['date']
        except:
            pass

        try:
            if(request.POST['inTime']!=""):
                if(request.POST['statusRadio']) == "1":
                    log.emp_in_time = request.POST['inTime']
                else:
                    log.emp_in_time = None
        except:
            pass

        try:
            if(request.POST['outTime']!=""):
                if(request.POST['statusRadio']) == "1":
                    log.emp_out_time = request.POST['outTime']
                else:
                    log.emp_out_time = None
        except Exception as e:
            print(e)

        try:
            log.save()
            message_text = "Sucessfully updated the log."
            messages.success(request, message_text)
        except Exception as e:
            print(e)
            message_text = "Failed to update the log. Please try again."
            messages.error(request, message_text)

    return redirect('dashboard')

@login_required(login_url='user/login/')
def download(request):
    if(request.method == "POST"):
        response = HttpResponse('')
        print(request.POST)
        try:
            from_date = request.POST['from'] + "-01"
            to_date = request.POST['to'].split("-")

            test_date = datetime.date(int(to_date[0]),int(to_date[1]),4)
              
            
            # getting next month
            # using replace to get to last day + offset
            # to reach next month
            nxt_mnth = test_date.replace(day=28) + datetime.timedelta(days=4)
            
            # subtracting the days from next month date to
            # get last date of current Month
            res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
            
            # printing result
            print("Last date of month : " + str(res.day))
            to_date = datetime.date(int(to_date[0]),int(to_date[1]),res.day)
            print(to_date)
            
            try:
                if (request.POST['allEmpCheck'] == "1"):
                    allEmpDownload = True
                else:
                    allEmpDownload = False
            except:
                allEmpDownload = False

            if (allEmpDownload):
                print("IN IF")
                data = attendanceLog.objects.filter(date__gte=from_date,date__lte=to_date)
                response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename='+"CredoSense_Attendance_Log_All_"+ str(from_date)+'_to_'+str(to_date)+".csv"},)
                # print(data)
            
            else:
                print("IN ELSE")
                print(request.POST['empname'])
                emp_id = str(request.POST['empname']).split("(")
                emp_id = emp_id[1].replace(")" , "")
                print("Emo ID" , emp_id)
                data = attendanceLog.objects.filter(emp = emp_id, date__gte=from_date,date__lte=to_date)
                response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename='+"CredoSense_Attendance_Log_"+ emp_id +"_"+ str(from_date)+'_to_'+str(to_date)+".csv"},)
                print(data)

            if not data:
                print("NO DATA")
                message_text = "No data found for the selected dates or employee. Please try again."
                messages.error(request, message_text)
                return redirect('attendance-download')

            writer = csv.writer(response)
            writer.writerow(['CredoSense Inc. (Ltd.)'])
            writer.writerow(['Attendance Log:' , str(from_date) + " to " + str(to_date)])
            if(allEmpDownload):
                writer.writerow(['Employee:' , 'Everyone'])
            else:
                writer.writerow(['Employee:' , request.POST['empname']])

            writer.writerow([])
            print(response)
            return response
        except Exception as e:
            print("Exception: ", e)

    
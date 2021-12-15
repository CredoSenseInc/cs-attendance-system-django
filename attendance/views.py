from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import attendanceLog
from datetime import date
import datetime
from django.contrib import messages

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
            log.emp_in_time = request.POST['inTime']
        except:
            pass

        try:
            log.emp_out_time = request.POST['outTime']
        except:
            pass

        try:
            log.save()
            message_text = "Sucessfully updated the log."
            messages.success(request, message_text)
        except:
            message_text = "Failed to update the log. Please try again."
            messages.error(request, message_text)

    return redirect('dashboard')
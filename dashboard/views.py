from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import *
from datetime import date

# Create your views here.
@login_required(login_url='user/login/')
def dashboard(request):
    todays_date = date.today()
    log_list = attendanceLog.objects.filter(date__month=todays_date.month)
    daily_log_list = attendanceLog.objects.filter(date=todays_date)
    context = {
        "log_list" : log_list,
        "daily_log_list" : daily_log_list
    }
    return render(request, 'dashboard/dashboard.html', context)
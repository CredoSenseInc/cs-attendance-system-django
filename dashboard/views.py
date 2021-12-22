from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import *
from settings.models import *
from datetime import date
import datetime

# Create your views here.
@login_required(login_url='user/login/')
def dashboard(request):
    todays_date = date.today()
    log_list = attendanceLog.objects.filter(date__month=todays_date.month)
    daily_log_list = attendanceLog.objects.filter(date=todays_date)
    total_emp = employee.objects.all().count()
    settings = settings_db.objects.last()
    if (settings is None):
        settings = settings_db()
        settings.save()
        settings = settings_db.objects.last()

    present_count = attendanceLog.objects.filter(date=todays_date, emp_present = True).count()
    
    late_count = attendanceLog.objects.filter(date=todays_date, emp_present = True, emp_in_time__gte = settings_db.objects.last().delayTime).count()
    # print(settings_db.objects.last().delayTime)
    absent_count = attendanceLog.objects.filter(date=todays_date, emp_present = False).count()
    now = datetime.datetime.now()

    # current_time = now.strftime("%H:%M:%S")
    # print(current_time , settings.endTime)
    context = {
        "log_list" : log_list,
        "daily_log_list" : daily_log_list,
        "current_month" : (todays_date).strftime("%B"),
        "current_date" : (todays_date).strftime("%d-%b-%Y"),
        "total_emp" : total_emp,
        "present_count" : present_count,
        "late_count" : late_count,
        "absent_count" : absent_count,
        "late_time" : settings.delayTime,
        "end_time": settings.endTime,
        # "current_time" : current_time
    }
    create_daily_log(request)
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='user/login/')
def create_daily_log(request):
    todays_date = date.today()
    print(todays_date)
    all_emp = employee.objects.all()
    settings = settings_db.objects.last()
    offDay = str(settings.offDay).split(",")
    workDay = str(settings.workDay).split(",")
    print(workDay)

    for i in range (len(offDay)):
        if(offDay[i]!=''):
            offDay[i] = datetime.datetime.strptime(offDay[i], '%m/%d/%Y').date()
        # offDay[i] = datetime.datetime.strptime(offDay[i], '%Y-%m-%d').date()
        # print(offDay[i])

    for i in range (len(workDay)):
        if(workDay[i]!=''):
            workDay[i] = datetime.datetime.strptime(workDay[i], '%m/%d/%Y').date()
        # workDay[i] = datetime.datetime.strptime(workDay[i], '%Y-%m-%d').date()
        # print(offDay[i])
    weekends = []

    if settings.week_saturday:
        weekends.append("Saturday")
    if settings.week_sunday:
        weekends.append("Sunday")
    if settings.week_monday:
        weekends.append("Monday")
    if settings.week_tuesday:
        weekends.append("Tuesday")
    if settings.week_wednesday:
        weekends.append("Wednesday")
    if settings.week_thursday:
        weekends.append("Thursday")
    if settings.week_friday:
        weekends.append("Friday")

    print(todays_date.strftime('%A'))
    print(weekends)

    if (todays_date.strftime('%A') in weekends):
        if(todays_date in workDay):
            all_emp = employee.objects.all()
            check_today_log = attendanceLog.objects.filter(date = todays_date).count()
            print(check_today_log)
            if (check_today_log == 0):
                for i in range (len(all_emp)):
                    attendance = attendanceLog()
                    attendance.emp = all_emp[i]
                    attendance.finger1 = all_emp[i]
                    attendance.date = todays_date
                    attendance.save()

    elif(todays_date in offDay):
        # weekend
        pass
    else:
        all_emp = employee.objects.all()
        check_today_log = attendanceLog.objects.filter(date = todays_date).count()
        print(check_today_log)
        if (check_today_log == 0):
            for i in range (len(all_emp)):
                attendance = attendanceLog()
                attendance.emp = all_emp[i]
                attendance.finger1 = all_emp[i]
                attendance.date = todays_date
                attendance.save()   


    if (todays_date.strftime('%A') in weekends or todays_date in offDay and todays_date not in workDay):
        print("Today is weekend")
    
    elif(todays_date.strftime('%A') not in weekends or todays_date not in offDay and todays_date  in workDay):
        print("Today is workday")
        all_emp = employee.objects.all()
        check_today_log = attendanceLog.objects.filter(date = todays_date).count()
        print(check_today_log)
        if (check_today_log == 0):
            for i in range (len(all_emp)):
                attendance = attendanceLog()
                attendance.emp = all_emp[i]
                attendance.finger = all_emp[i]
                attendance.date = todays_date
                attendance.save()
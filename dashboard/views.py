from telnetlib import STATUS
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import *
from settings.models import *
from datetime import date
import datetime
# from rest_framework.authtoken.models import Token

def dashboard_view(request):
    # token = Token.objects.create(user=request.user)
    todays_date = date.today()
    log_list = attendanceLog.objects.filter(date__month=todays_date.month)
    daily_log_list = attendanceLog.objects.filter(date=todays_date)
    present_emp = daily_log_list.filter(emp_present = True)
    abesent_emp = daily_log_list.filter(emp_present = False)
    late_emp = daily_log_list.filter(date=todays_date, emp_present = True, emp_in_time__gte = settings_db.objects.last().delayTime)

    

    total_emp = employee.objects.all().count()
    settings = settings_db.objects.last()
    if (settings is None):
        settings = settings_db()
        settings.save()
        settings = settings_db.objects.last()

    additonal_off_days = settings.offDay.split(",")
    additional_work_days = settings.workDay.split(",")

    for i in range(len(additional_work_days)):
        try:
            additional_work_days[i] = datetime.datetime.strptime(additional_work_days[i], '%m/%d/%Y')
        except:
            pass


    for i in range(len(additonal_off_days)):
        additonal_off_days[i] = datetime.datetime.strptime(additonal_off_days[i], '%m/%d/%Y')
        try:
            if additonal_off_days[i] in additional_work_days:
                additonal_off_days.pop(i)
        except:
            pass

    


    print("------------")
    print("Off days11" , additonal_off_days)
    print("------------")
    present_count = attendanceLog.objects.filter(date=todays_date, emp_present = True).count()
    
    late_count = attendanceLog.objects.filter(date=todays_date, emp_present = True, emp_in_time__gte = settings_db.objects.last().delayTime).count()
    # print(settings_db.objects.last().delayTime)
    absent_count = attendanceLog.objects.filter(date=todays_date, emp_present = False).count()
    now = datetime.datetime.now()

    present_graph = []
    present_graph_name = []
    late_graph = []
    late_graph_name = []
    absent_graph = []
    absent_graph_name = []
    not_signed_out_graph = []
    not_signed_out_graph_name = []
    all_emp = employee.objects.all()

    for i in range (all_emp.count()):
        present_graph_name.append(all_emp[i].emp_name)
        present_graph.append(log_list.filter(emp = all_emp[i], emp_present = True).exclude(date__in = additonal_off_days).count())


    for i in range (all_emp.count()):
        late_graph_name.append(all_emp[i].emp_name)
        late_graph.append(log_list.filter(emp = all_emp[i], emp_present = True, emp_in_time__gte = settings_db.objects.last().delayTime).exclude(date__in = additonal_off_days).count())


    for i in range (all_emp.count()):
        absent_graph_name.append(all_emp[i].emp_name)
        absent_graph.append(log_list.filter(emp = all_emp[i], emp_present = False).exclude(date__in = additonal_off_days).count())


    for i in range (all_emp.count()):
        not_signed_out_graph_name.append(all_emp[i].emp_name)
        not_signed_out_graph.append(log_list.filter(emp = all_emp[i], emp_present = True, emp_in_time__isnull=False, emp_out_time__isnull=True).exclude(date__in = additonal_off_days).count())

    show_table = create_daily_log()

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
        "present_emp" : present_emp,
        "abesent_emp" : abesent_emp,
        "late_emp" : late_emp,
        "present_graph" : present_graph,
        "present_graph_name" : present_graph_name,
        "late_graph" : late_graph,
        "late_graph_name" : late_graph_name,
        "absent_graph" : absent_graph,
        "absent_graph_name" : absent_graph_name,
        "not_signed_out_graph" : not_signed_out_graph,
        "not_signed_out_graph_name" : not_signed_out_graph_name,
        "show_table" : show_table

        # "current_time" : current_time
    }
    
    return render(request, 'dashboard/dashboard_view.html', context)

# Create your views here.
@login_required(login_url='/user/login/')
def dashboard(request):
    # token = Token.objects.create(user=request.user)
    todays_date = date.today()
    log_list = attendanceLog.objects.filter(date__month=todays_date.month)
    daily_log_list = attendanceLog.objects.filter(date=todays_date)
    present_emp = daily_log_list.filter(emp_present = True)
    abesent_emp = daily_log_list.filter(emp_present = False)
    late_emp = daily_log_list.filter(date=todays_date, emp_present = True, emp_in_time__gte = settings_db.objects.last().delayTime)

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
    show_table = create_daily_log()
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
        "present_emp" : present_emp,
        "abesent_emp" : abesent_emp,
        "late_emp" : late_emp,
        "show_table" : show_table,

        # "current_time" : current_time
    }
    print("SHOW TABLE " , show_table)
    return render(request, 'dashboard/dashboard.html', context)



# @login_required(login_url='/user/login/')
def create_daily_log():
    print("Creating daily log")
    todays_date = date.today()
    print(todays_date)
    print(datetime.datetime.now().strftime("%H:%M:%S"))
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
                
    # check_today_log = attendanceLog.objects.filter(date = todays_date).count()
    
    # if check_today_log > 0:
    #     show_table = True
    # else:
    #     show_table = False


    show_table = True
    if (todays_date.strftime('%A') in weekends):
        show_table = False
        if(todays_date in workDay):
            show_table = True
    elif(todays_date in offDay):
        show_table = False
    else:
        show_table = True
    return show_table
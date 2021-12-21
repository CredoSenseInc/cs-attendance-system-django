from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from attendance.models import attendanceLog
from datetime import date
import datetime
from django.contrib import messages
import csv
from employee.models import employee
from settings.models import *
from django.http import HttpResponseRedirect

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
    next = request.POST.get('next', '/')
    try:
        if(request.POST['next'] == "/attendance/view"):
            return redirect('attendance-download')
        else:
            return HttpResponseRedirect(next)
    except:
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

            settings = settings_db.objects.last()
            if (allEmpDownload):
                print("IN IF")
                data = attendanceLog.objects.filter(date__gte=from_date,date__lte=to_date).order_by("date", "emp__emp_name")
                
                print(from_date)
                print(to_date)
                if(request.POST['button'] == "view"):
                    context = {
                        "log_list" : data,
                        "from_date" : datetime.datetime.strptime(str(from_date), '%Y-%m-%d').date(),
                        "to_date" : datetime.datetime.strptime(str(to_date), '%Y-%m-%d').date(),
                    }
                    return render(request, 'download/view.html', context)

                empList = employee.objects.all().order_by("emp_name")
                emp_name_csv = "Everyone"
                response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename='+"CredoSense_Attendance_Log_All_"+ str(from_date)+'_to_'+str(to_date)+".csv"},)
                # print(data)
            
            else:
                print("IN ELSE")
                print(request.POST['empname'])
                emp_id = str(request.POST['empname']).split("(")
                emp_id = emp_id[1].replace(")" , "")
                print("Emp ID" , emp_id)
                data = attendanceLog.objects.filter(emp = emp_id, date__gte=from_date,date__lte=to_date)
                if(request.POST['button'] == "view"):
                    context = {
                        "log_list" : data,
                        "from_date" : datetime.datetime.strptime(str(from_date), '%Y-%m-%d').date(),
                        "to_date" : datetime.datetime.strptime(str(to_date), '%Y-%m-%d').date(),
                    }
                    return render(request, 'download/view.html', context)
                    
                empList = employee.objects.filter(emp_id = emp_id).order_by("emp_name")
                emp_name_csv = request.POST['empname']
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
            # if(allEmpDownload):
            writer.writerow(['Employee:' , emp_name_csv])
            writer.writerow([])
            writer.writerow(['Name' ,'ID', 'Present Count' , 'Late Count' , 'Absent Count', 'Early leave', 'Salary type', 'Salary', 'Overtime/hr', 'Total overtime', 'Total workhour', 'Total Salary'])
            
            print("___")
            for i in range(len(empList)):
                present_count = data.filter(emp = empList[i], emp_present = True).count()

                abs_count = data.filter(emp = empList[i], emp_present = False).count()

                late_count = data.filter(emp = empList[i], emp_present = True, emp_in_time__gte=settings.delayTime).count()

                early_count = data.filter(emp = empList[i], emp_present = True, emp_out_time__lte=settings.endTime).count()
                overtime = datetime.timedelta()
                tottalworktime = datetime.timedelta()
                total_salary = float(empList[i].emp_salary)
                
                    
                overtime_data = data.filter(emp = empList[i], emp_present = True, emp_out_time__gte = settings.endTime)

                for j in range(len(overtime_data)):
                    time_diff = datetime.datetime.combine(overtime_data[j].date, overtime_data[j].emp_out_time) - datetime.datetime.combine(overtime_data[j].date, settings.endTime)
                    (h, m, s) = str(time_diff).split(':')
                    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    overtime += d

                work_data = data.filter(emp = empList[i], emp_present = True).exclude(emp_in_time=None).exclude(emp_out_time=None)

                for k in range(len(work_data)):
                    duration = str(datetime.datetime.combine(work_data[k].date, work_data[k].emp_out_time) - datetime.datetime.combine(work_data[k].date,work_data[k].emp_in_time))
                    print(empList[i].emp_name,duration)
                    (h, m, s) = str(duration).split(':')
                    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    tottalworktime += d

                worktime = tottalworktime - overtime

                if(empList[i].emp_salary_type == "M"):
                    total_salary = round(float(total_salary) +  float(overtime.total_seconds()/3600) * float(empList[i].emp_overtime_per_hour) , 2)
                elif(empList[i].emp_salary_type == "H"):
                    total_salary = round(float(total_salary) * (float(worktime.total_seconds()/3600)) +  float(overtime.total_seconds()/3600) * float(empList[i].emp_overtime_per_hour) , 2)
                
                    
                #     total_salary = float(total_salary) +  float(overtime.total_seconds()/3600) * float(empList[i].emp_overtime_per_hour)

                writer.writerow([empList[i].emp_name , empList[i].emp_id,  present_count , late_count , abs_count, early_count, "Monthly" if empList[i].emp_salary_type == "M" else "Hourly", empList[i].emp_salary, empList[i].emp_overtime_per_hour, str(overtime) + " hrs", str(tottalworktime)+ " hrs" , total_salary])
            writer.writerow([])
            writer.writerow([])
            writer.writerow(['Name' ,'ID', 'Date' , 'Status', 'In time' ,  'Out time', 'Overtime', 'Total workhour',])
            

            for i in range (len(data)):
                overtime = "0 hrs"
                duration = "0 hrs"
                status = "Absent"
                
                try:
                    # print(datetime.datetime.combine(data[i].date, data[i].emp_out_time) - datetime.datetime.combine(data[i].date, data[i].emp_in_time))
                    duration = str(datetime.datetime.combine(data[i].date, data[i].emp_out_time) - datetime.datetime.combine(data[i].date, data[i].emp_in_time)) + " hrs"
                    
                    if(data[i].emp_out_time > settings.endTime):
                        overtime = str(datetime.datetime.combine(data[i].date, data[i].emp_out_time) - datetime.datetime.combine(data[i].date, settings.endTime)) + " hrs"
                    if(data[i].emp_present):
                        status = "Present"
                        if(data[i].emp_in_time > settings.delayTime):
                            status = status + " (Late)"
                        if(data[i].emp_out_time < settings.endTime):
                            status = status + " & Left early"
                        elif (data[i].emp_out_time >= settings.endTime):
                            status = status + " & Signed out"


                except:
                    duration = ""
                    overtime = ""

                writer.writerow([data[i].emp.emp_name, data[i].emp.emp_id,
                data[i].date,
                status,
                data[i].emp_in_time,
                data[i].emp_out_time,
                str(overtime),
                duration,
                
                ])
                   
            # else:
            #     writer.writerow(['Employee:' , request.POST['empname']])

            writer.writerow([])
            print(response)
            return response
        except Exception as e:
            print("Exception: ", e)
            message_text = "No data found for the selected dates or employee. Please try again."
            messages.error(request, message_text)
            return redirect('attendance-download')

    
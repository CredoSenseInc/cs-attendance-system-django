from django.http import response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from employee.models import *
from device.models import *
from django.db.models import Q
from django.contrib import messages
from attendance.models import *
from settings.models import *
from datetime import date
import datetime
# Create your views here.

@login_required(login_url='user/login/')
def employee_page(request):
    emp_list = employee.objects.all()
    device_list = deviceInfo.objects.all()
    context = {
        "emp_list" : emp_list,
        "device_list" : device_list,
    }
    return render(request, 'employee/employee.html', context)

@login_required(login_url='user/login/')
def add_emp(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        try:
            
            emp = employee()
            emp.emp_name = request.POST['name']
            emp.emp_contact_number = request.POST['number']
            emp.emp_id = request.POST['id']
            # emp.emp_finger_id_1 = 
            emp.emp_gender = request.POST['gender']
            emp.emp_designation = request.POST['designation']
            emp.emp_dept = request.POST['dept']
            emp.emp_salary_type = request.POST['salaryType']
            emp.emp_salary= request.POST['salary']
            emp.emp_overtime_per_hour = request.POST['oversalary']
            
            emp.save()

            deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
            message_text = "Sucessfully added new employee."
            messages.success(request, message_text)

            attendance = attendanceLog()
            attendance.emp = emp
            attendance.finger1 = emp
            attendance.date = date.today()
            attendance.save()


            # scan_fingerprint(emp.emp_finger_id_1, request.POST['device'], request)

        except Exception as e:
            print(e)
            message_text = "Failed to add employee. Please try again."
            messages.error(request, message_text)
    return redirect('employee')

@login_required(login_url='user/login/')
def update_emp(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        try:
            emp = employee.objects.get(id = request.POST['id'])
            if(request.POST['button'] == "rescan1"):
                scan_fingerprint(emp.emp_finger_id_1, request.POST['device'], request)
            
            elif(request.POST['button'] == "rescan2"):
                if(emp.emp_finger_id_2 == ""):
                    emp.emp_finger_id_2 = generate_unique_fid()
                    emp.save()
                    deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
                scan_fingerprint(emp.emp_finger_id_2, request.POST['device'], request)
            
            elif(request.POST['button'] == "rescan3"):
                if(emp.emp_finger_id_3 == ""):
                    emp.emp_finger_id_3 = generate_unique_fid()
                    emp.save()
                    deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
                scan_fingerprint(emp.emp_finger_id_3, request.POST['device'], request)
            
            elif(request.POST['button'] == "rescan4"):
                if(emp.emp_finger_id_4 == ""):
                    emp.emp_finger_id_4 = generate_unique_fid()
                    emp.save()
                    deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
                scan_fingerprint(emp.emp_finger_id_4, request.POST['device'], request)
            
            elif(request.POST['button'] == "rescan1-delete"):
                delete_fingerprint([emp.emp_finger_id_1])
                emp.emp_finger_id_1 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Sucessfully updated employee information."
                messages.success(request, message_text)

            elif(request.POST['button'] == "rescan2-delete"):
                delete_fingerprint([emp.emp_finger_id_2])
                emp.emp_finger_id_2 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Sucessfully updated employee information."
                messages.success(request, message_text)
                
            elif(request.POST['button'] == "rescan3-delete"):
                delete_fingerprint([emp.emp_finger_id_3])
                emp.emp_finger_id_3 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Sucessfully updated employee information."
                messages.success(request, message_text)
            
            elif(request.POST['button'] == "rescan4-delete"):
                delete_fingerprint([emp.emp_finger_id_4])
                emp.emp_finger_id_4 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Sucessfully updated employee information."
                messages.success(request, message_text)

            elif(request.POST['button'] == "delete"):
                fingerprints = []
                if(emp.emp_finger_id_1 != ""):
                        deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                        fingerprints.append(emp.emp_finger_id_1)
                if(emp.emp_finger_id_2 != ""):
                    deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                    fingerprints.append(emp.emp_finger_id_2)
                if(emp.emp_finger_id_3 != ""):
                    deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                    fingerprints.append(emp.emp_finger_id_3)
                if(emp.emp_finger_id_4 != ""):
                    deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                    fingerprints.append(emp.emp_finger_id_4)
                emp.delete()
                delete_fingerprint(fingerprints)
                message_text = "Sucessfully removed " + emp.emp_name + " (ID: " + emp.emp_id + ") from the system."
                messages.success(request, message_text)
            else:
                # emp = employee.objects.get(id = request.POST['id'])
                emp.emp_name = request.POST['name']
                emp.emp_contact_number = request.POST['number']
                # emp.emp_id = request.POST['id']
                # emp.emp_finger_id_1 = 
                emp.emp_gender = request.POST['gender']
                emp.emp_designation = request.POST['designation']
                emp.emp_dept = request.POST['dept']
                emp.emp_salary_type = request.POST['salaryType']
                emp.emp_salary= request.POST['salary']
                emp.emp_overtime_per_hour = request.POST['oversalary']
                emp.save()
                message_text = "Sucessfully updated employee information."
                messages.success(request, message_text)
        except Exception as e:
            print(e)
            message_text = "Failed to update employee information. Please try again."
            messages.error(request, message_text)
    return redirect('employee')

def delete_fingerprint(fingerprints):

    devices = deviceInfo.objects.all()
    for i in range (len(devices)):
        for j in range (len(fingerprints)):
            print("Finger id:" , fingerprints[j])
            cmd = commands()
            cmd.device_id = devices[i]
            cmd.message = "delete:"+ str(fingerprints[j])
            cmd.save()

# @login_required(login_url='user/login/')
def scan_fingerprint(fid, device, request):
    try:
        cmd = commands()
        cmd.device_id = deviceInfo.objects.get(device_id = device)
        cmd.message = "scan:"+ str(fid)
        cmd.save()
        json_id = cmd.id
        timeout = time.time() + 60
        while(True):
            check = commands.objects.get(id = json_id)
            if(check.isExecuted):
                message_text = "Sucessfully updated employee information."
                messages.success(request, message_text)
                break

            if time.time() > timeout:
                message_text = "Failed to commiunicate with the device. Please try again."
                messages.error(request, message_text)
                check.server_message = "Failed to commiunicate with ESP"
                check.isExecuted = True
                check.save()
                break
            
        
        # message_text = "Please check the finger print device and follow instructions to scan fingeprint."
        # messages.warning(request, message_text)
    except Exception as e:
        print("Exception: ", e)
        message_text = "Failed to get fingerprint from the device. Please try again."
        messages.error(request, message_text)

    # return redirect('employee')


@login_required(login_url='user/login/')
def attendance_download(request):
    todays_date = date.today()
    today = date.today()
    lastMonth = today.replace(day=1) - datetime.timedelta(days=1)
    print(lastMonth.strftime("%m"))
    print(todays_date.month)

    emp = employee.objects.values_list('emp_name', flat=True)
    log_list = attendanceLog.objects.filter(date__month__lte=todays_date.month, date__month__gte=lastMonth.month)
    settings = settings_db.objects.last()
    context = {
        "emp" : emp,
        "log_list" : log_list,
        "current_month" : (todays_date).strftime("%B"),
        "last_month" : (lastMonth).strftime("%B"),
        "late_time" : settings.delayTime,
        "end_time": settings.endTime,
    }
    return render(request, 'download/download.html', context)

@login_required(login_url='user/login/')
def attendance_download_search(request):
    if "term" in request.GET:
        qs = employee.objects.filter(Q(emp_name__icontains=request.GET.get("term")) | Q(emp_id__icontains=request.GET.get("term")))
        result = list()
        for i in qs:
            result.append(i.emp_name + " (" + i.emp_id + ")")
        return response.JsonResponse(result, safe=False)
    # return render(request, 'download/download.html', context)
from email import message
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
import calendar
# Create your views here.

@login_required(login_url='/user/login/')
def employee_page(request):
    emp_list = employee.objects.all()
    device_list = deviceInfo.objects.all()
    context = {
        "emp_list" : emp_list,
        "device_list" : device_list,
    }
    return render(request, 'employee/employee.html', context)

@login_required(login_url='/user/login/')
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
            # emp.emp_salary_type = request.POST['salaryType']
            # emp.emp_salary= request.POST['salary']
            # emp.emp_overtime_per_hour = request.POST['oversalary']
            emp.email = request.POST['email']
            
            emp.save()

            deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
            message_text = "Successfully added new employee."
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

# Fingerprint update portion is same as CS_MGT settings > views.py > def fingerprint_manage 
@login_required(login_url='/user/login/')
def update_emp(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        try:
            emp = employee.objects.get(id = request.POST['id'])
            if(request.POST['button'] == "rescan1"):
                device = deviceInfo.objects.get(device_id = request.POST['device'])
                if(device.device_emp_count > 0):
                    delete_fingerprint([emp.emp_finger_id_1])
                    scan_fingerprint(emp.emp_finger_id_1, request.POST['device'], request)
                else:
                    message_text = "Failed to update employee information. Finger print device reached max capacity."
                    messages.error(request, message_text)
            
            elif(request.POST['button'] == "rescan2"):
                device = deviceInfo.objects.get(device_id = request.POST['device'])
                if(device.device_emp_count > 0):
                    if(emp.emp_finger_id_2 == ""):
                        emp.emp_finger_id_2 = generate_unique_fid()
                        emp.save()
                        deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
                    delete_fingerprint([emp.emp_finger_id_2])
                    scan_fingerprint(emp.emp_finger_id_2, request.POST['device'], request)
                else:
                    message_text = "Failed to update employee information. Finger print device reached max capacity."
                    messages.error(request, message_text)
            
            elif(request.POST['button'] == "rescan3"):
                device = deviceInfo.objects.get(device_id = request.POST['device'])
                if(device.device_emp_count > 0):
                    if(emp.emp_finger_id_3 == ""):
                        emp.emp_finger_id_3 = generate_unique_fid()
                        emp.save()
                        deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
                    delete_fingerprint([emp.emp_finger_id_3])
                    scan_fingerprint(emp.emp_finger_id_3, request.POST['device'], request)
                else:
                    message_text = "Failed to update employee information. Finger print device reached max capacity."
                    messages.error(request, message_text)
            
            elif(request.POST['button'] == "rescan4"):
                device = deviceInfo.objects.get(device_id = request.POST['device'])
                if(device.device_emp_count > 0):
                    if(emp.emp_finger_id_4 == ""):
                        emp.emp_finger_id_4 = generate_unique_fid()
                        emp.save()
                        deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') - 1)
                    delete_fingerprint([emp.emp_finger_id_4])
                    scan_fingerprint(emp.emp_finger_id_4, request.POST['device'], request)
                else:
                    message_text = "Failed to update employee information. Finger print device reached max capacity."
                    messages.error(request, message_text)
            
            elif(request.POST['button'] == "rescan1-delete"):
                delete_fingerprint([emp.emp_finger_id_1])
                emp.emp_finger_id_1 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Successfully updated employee information."
                messages.success(request, message_text)

            elif(request.POST['button'] == "rescan2-delete"):
                delete_fingerprint([emp.emp_finger_id_2])
                emp.emp_finger_id_2 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Successfully updated employee information."
                messages.success(request, message_text)
                
            elif(request.POST['button'] == "rescan3-delete"):
                delete_fingerprint([emp.emp_finger_id_3])
                emp.emp_finger_id_3 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Successfully updated employee information."
                messages.success(request, message_text)
            
            elif(request.POST['button'] == "rescan4-delete"):
                delete_fingerprint([emp.emp_finger_id_4])
                emp.emp_finger_id_4 = ""
                emp.save()
                deviceInfo.objects.all().update(device_emp_count=F('device_emp_count') + 1)
                message_text = "Successfully updated employee information."
                messages.success(request, message_text)

            elif(request.POST['button'] == "delete"):
                if emp.rfid_tag_number != -1:
                    delete_rfid(emp.rfid_tag_number)
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
                message_text = "Successfully removed " + emp.emp_name + " (ID: " + emp.emp_id + ") from the system."
                messages.success(request, message_text)

            

            # Employee data update
            else:
                # emp = employee.objects.get(id = request.POST['id'])
                emp.emp_name = request.POST['name']
                emp.emp_contact_number = request.POST['number']
                # emp.emp_id = request.POST['id']
                # emp.emp_finger_id_1 = 
                emp.emp_gender = request.POST['gender']
                emp.emp_designation = request.POST['designation']
                emp.emp_dept = request.POST['dept']
                # emp.emp_salary_type = request.POST['salaryType']
                # emp.emp_salary= request.POST['salary']
                # emp.emp_overtime_per_hour = request.POST['oversalary']

                try:
                    emp.email = request.POST['email']
                except:
                    pass
                
                previous_rfid = emp.rfid_tag_number
                # if int(request.POST['rfid']) != emp.rfid_tag_number:
                #     delete_rfid(emp.rfid_tag_number)

                try:
                    emp.rfid_tag_number = request.POST['rfid'] if request.POST['rfid'] != None else None
                    

                    if (emp.rfid_tag_number == ""):
                        emp.rfid_tag_number = None

                    new_rfid = emp.rfid_tag_number

                    print("----")
                    print(new_rfid)
                except Exception as e:
                    
                    print(e)
                    pass
                
                emp.save()

                    
                if previous_rfid is None and new_rfid is not None:
                    # no need to delete the previous rfid
                    save_rfid(new_rfid)

                elif new_rfid is None and previous_rfid is not None:
                    # no need to save the new rfid
                    delete_rfid(previous_rfid)

                elif new_rfid != previous_rfid:
                    delete_rfid(previous_rfid)
                    save_rfid(new_rfid)
                
                else:
                    pass


                message_text = "Successfully updated employee information."
                messages.success(request, message_text)
        except Exception as e:
            print(e)
            message_text = "Failed to update employee information. Please try again."
            messages.error(request, message_text)
    return redirect('employee')

# Send the delete command to all the device
def delete_fingerprint(fingerprints):

    devices = deviceInfo.objects.all()
    for i in range (len(devices)):
        for j in range (len(fingerprints)):
            print("Finger id:" , fingerprints[j])
            cmd = commands()
            cmd.device_id = devices[i]
            cmd.message = "delete:"+ str(fingerprints[j])
            cmd.save()


# Send the delete command to delete the rfid tag number to all the device
def delete_rfid(rfid):
    devices = deviceInfo.objects.all()
    for i in range (len(devices)):     
        print("RFID : " , rfid)
        cmd = commands()
        cmd.device_id = devices[i]
        cmd.message = "delete_rfid:"+ str(rfid)
        cmd.save()

# Send the delete command to save the rfid tag number to all the device
def save_rfid(rfid):
    devices = deviceInfo.objects.all()
    for i in range (len(devices)):     
        print("RFID : " , rfid)
        cmd = commands()
        cmd.device_id = devices[i]
        cmd.message = "save_rfid:"+ str(rfid)
        cmd.save()


# @login_required(login_url='/user/login/')
# Method to send scan the fingerprint command 
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
                message_text = "Successfully updated employee information."
                messages.success(request, message_text)
                
                devices = deviceInfo.objects.all()
                for i in range (len(devices)):
                    if (devices[i] == cmd.device_id):
                        pass
                    else:
                        cmd2 = commands()
                        cmd2.device_id = devices[i]
                        cmd2.message = "scan:-99"
                        cmd2.save()
                
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

# Emp attendance download page
@login_required(login_url='/user/login/')
def attendance_download(request):
    todays_date = date.today()

    # Date for filter/download form
    lastMonth = (date.today().replace(day=1) - datetime.timedelta(days =1)).replace(day = 1)
    todayMonth = date.today().replace(day=calendar.monthrange(todays_date.year, todays_date.month)[1])
    
    print(lastMonth)
    print(todayMonth)
    emp = employee.objects.values_list('emp_name', flat=True)
    emp_list = employee.objects.all()
    log_list = attendanceLog.objects.filter(date__lte=todayMonth, date__gte=lastMonth)
    settings = settings_db.objects.last()
    
    print("Log List " , log_list)
    context = {
        "emp" : emp,
        "log_list" : log_list,
        "current_month" : (todays_date).strftime("%B"),
        "last_month" : (lastMonth).strftime("%B"),
        "late_time" : settings.delayTime,
        "end_time": settings.endTime,
        "emp_list" : emp_list
    }
    return render(request, 'download/download.html', context)

# Search for the dropdown. AJAX request
@login_required(login_url='/user/login/')
def attendance_download_search(request):
    if "term" in request.GET:
        qs = employee.objects.filter(Q(emp_name__icontains=request.GET.get("term")) | Q(emp_id__icontains=request.GET.get("term")))
        result = list()
        for i in qs:
            result.append(i.emp_name + " (" + i.emp_id + ")")
        return response.JsonResponse(result, safe=False)
    # return render(request, 'download/download.html', context)
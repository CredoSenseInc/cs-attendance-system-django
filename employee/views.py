from django.http import response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from employee.models import *
from device.models import *
from django.db.models import Q
from django.contrib import messages
# Create your views here.

@login_required(login_url='user/login/')
def employee_page(request):
    emp_list = employee.objects.all()
    context = {
        "emp_list" : emp_list
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
            # emp.emp_finger_id = 
            emp.emp_gender = request.POST['gender']
            emp.emp_designation = request.POST['designation']
            emp.emp_dept = request.POST['dept']
            emp.emp_salary_type = request.POST['salaryType']
            emp.emp_salary= request.POST['salary']
            emp.emp_overtime_per_hour = request.POST['oversalary']
            emp.save()
            message_text = "Sucessfully added new employee."
            messages.success(request, message_text)
        except:
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
            emp.emp_name = request.POST['name']
            emp.emp_contact_number = request.POST['number']
            emp.emp_id = request.POST['id']
            # emp.emp_finger_id = 
            emp.emp_gender = request.POST['gender']
            emp.emp_designation = request.POST['designation']
            emp.emp_dept = request.POST['dept']
            emp.emp_salary_type = request.POST['salaryType']
            emp.emp_salary= request.POST['salary']
            emp.emp_overtime_per_hour = request.POST['oversalary']
            emp.save()
            message_text = "Sucessfully updated employee information."
            messages.success(request, message_text)
        except:
            message_text = "Failed to update employee information. Please try again."
            messages.error(request, message_text)
    return redirect('employee')

@login_required(login_url='user/login/')
def scan_fingerprint(request, fid):
    try:
        cmd = commands()
        cmd.device_id = deviceInfo.objects.get(device_id = "29EFA8")
        cmd.message = "scan:"+ str(fid)
        cmd.save()
        message_text = "Please check the finger print device and follow instructions to scan fingeprint."
        messages.warning(request, message_text)
    except Exception as e:
        print("Exception: ", e)
        message_text = "Failed to get fingerprint from the device. Please try again."
        messages.error(request, message_text)

    return redirect('employee')


@login_required(login_url='user/login/')
def attendance_download(request):
    emp = employee.objects.values_list('emp_name', flat=True)
    context = {
        "emp" : emp,
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
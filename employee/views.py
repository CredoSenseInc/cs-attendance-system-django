from django.http import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employee.models import *
from django.db.models import Q
# Create your views here.

@login_required(login_url='user/login/')
def employee_page(request):
    emp_list = employee.objects.all()
    context = {
        "emp_list" : emp_list
    }
    return render(request, 'employee/employee.html', context)

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
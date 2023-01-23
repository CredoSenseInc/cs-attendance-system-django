from django.shortcuts import render
from device.models import deviceInfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
@login_required(login_url='/user/login/')
def add_device(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        try:
            device = deviceInfo()

            device.device_name = request.POST['device-name']
            device.device_id = request.POST['device-id']
            device.device_location = request.POST['device-location']
            device.device_emp_count = request.POST['emp-count']
            device.firmware_version = "1.0.0"
            # device.device_deptartment = request.POST['dept']
            device.save()

        except Exception as e:
            print(e)
            message_text = "Failed to add Device. Please try again."
            messages.error(request, message_text)
    return redirect('settings')


# Edit your views here.
@login_required(login_url='/user/login/')
def edit_device(request):
    print(request.method)
    if request.method == "POST":

        print(request.POST)
        try:
            device = deviceInfo.objects.get(device_id = request.POST['device-id'])
            print(device)
            

            if request.POST['button']=="delete":
                print("delete")
                device.delete()
            elif request.POST['button']=="update":
                print("update")
                device.device_name = request.POST['device-name']
                device.device_location = request.POST['device-location']
                # device.device_emp_count = request.POST['emp-count']
                device.save()
            else:
                pass
                
                
        except Exception as e:
            print(e)
            message_text = "Failed to edit Device. Please try again."
            messages.error(request, message_text)
    return redirect('settings')
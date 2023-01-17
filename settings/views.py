from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from device.models import deviceInfo, firmware, commands
from settings.models import settings_db
from django.contrib import messages
import semantic_version

from django.db.models import Q
from rest_framework.authtoken.models import Token
# Create your views here.

# Create your views here.
# Configuring the overall settings.

# PLEASE CHECK CS_MGT Settings> Views.py > def settings
@login_required(login_url='/user/login/')
def settings(request):
    settings = settings_db.objects.last()
    device = deviceInfo.objects.all()
    firmware_version = firmware.objects.last()
    token = Token.objects.last()

    if(settings is None):
        settings = settings_db()
        settings.save()
    
    if(token is None):
        token = Token.objects.create(user=request.user)
        print(token)
    if(firmware_version is None):
        firmware_version = firmware()
        firmware_version.save()

    if(device is None):
        device = deviceInfo()
        device.save()

    update_all_button = False
    all_updated = True

    updateCommands = commands.objects.filter(Q(isExecuted = False, message__contains = "update"))
    # print(semantic_version.Version(str(firmware_version.version)))
    for d in device:
        if (semantic_version.Version(str(firmware_version.version)) > semantic_version.Version(str(d.firmware_version))):
            d.update_available = True
            all_updated = False
        
        check_update = updateCommands.filter(device_id = d)
        if len(check_update) > 0:
            d.is_updating = True
            update_all_button = True


    context = {
        "settings" : settings,
        "device" : device,
        "firmware_version" : firmware_version,
        "update_all_button" : update_all_button,
        "all_updated" : all_updated,
        "token" : token
    }
    return render(request, 'settings/settings.html', context)

# PLEASE CHECK CS_MGT Settings> Views.py > def firmware_update
@login_required(login_url='/user/login/')
def firmware_update(request):
    print(request.POST)
    if request.method == "POST":
        if request.POST["button"] == "firmware-update-all":
            try:
                firmware_version = firmware.objects.last()
                all_device = deviceInfo.objects.all()
                for device in all_device:
                    if (semantic_version.Version(str(firmware_version.version)) > semantic_version.Version(str(device.firmware_version))):
                        cmd = commands()
                        cmd.device_id = deviceInfo.objects.get(device_id = device.device_id)
                        cmd.message = "update:"+ str(firmware_version.url)
                        cmd.save()
                
                message_text = "Firmware update request has been sent to the device. Please wait for the device to get updated."
                messages.success(request, message_text)
            except Exception as e:
                print(e)
                message_text = "Failed to update firmware. Please try again."
                messages.error(request, message_text)

        else:
            try:
                firmware_version = firmware.objects.last()
                cmd = commands()
                cmd.device_id = deviceInfo.objects.get(device_id = request.POST["id"])
                cmd.message = "update:"+ str(firmware_version.url)
                cmd.save()

                message_text = "Firmware update request has been sent to the device. Please wait for the device to get updated."
                messages.success(request, message_text)
            except Exception as e:
                print(e)
                message_text = "Failed to update firmware. Please try again."
                messages.error(request, message_text)

    return redirect('settings')

# Update the settings value
@login_required(login_url='/user/login/')
def update(request):
    if request.method == "POST":
        settings = settings_db.objects.last()
        print(request.POST)
        try:
            settings.startTime = str(request.POST['start-time'])
        except:
            pass

        try:
            settings.endTime = str(request.POST['end-time'])
        except:
            pass
        
        try:
            settings.delayTime = str(request.POST['delay-time'])
        except:
            pass

        try:
            settings.offDay = str(request.POST['off-days'])
        except:
            pass

        try:
            settings.workDay = str(request.POST['work-days'])
        except:
            pass

        try:
            if(str(request.POST['week-saturday']) == 'on'):
                settings.week_saturday = True
            else:
                settings.week_saturday = False
        except:
            pass

        try:
            if(str(request.POST['week-sunday']) == 'on'):
                settings.week_sunday = True
            else:
                settings.week_sunday = False
        except:
            pass

        try:
            if(str(request.POST['week-monday']) == 'on'):
                settings.week_monday = True
            else:
                settings.week_monday = False
        except:
            pass

        try:
            if(str(request.POST['week-tuesday']) == 'on'):
                settings.week_tuesday = True
            else:
                settings.week_tuesday = False
        except:
            pass

        try:
            if(str(request.POST['week-wednesday']) == 'on'):
                settings.week_wednesday = True
            else:
                settings.week_wednesday = False
        except:
            pass

        try:
            if(str(request.POST['week-thursday']) == 'on'):
                settings.week_thursday = True
            else:
                settings.week_thursday = False
        except:
            pass

        try:
            if(str(request.POST['week-friday']) == 'on'):
                settings.week_friday = True
            else:
                settings.week_friday = False
        except:
            pass

        try:
            settings.save()
            message_text = "Successfully updated the settings."
            messages.success(request, message_text)
        except:
            message_text = "Failed to update the settings. Please try again."
            messages.error(request, message_text)
    # return render(request, 'settings/settings.html')
    return redirect('settings')
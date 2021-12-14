from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from settings.models import settings_db
from django.contrib import messages
# Create your views here.

@login_required(login_url='user/login/')
def settings(request):
    settings = settings_db.objects.last()
    
    if(settings is None):
        settings = settings_db()
        settings.save()

    context = {"settings" : settings}
    return render(request, 'settings/settings.html', context)

@login_required(login_url='user/login/')
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
            message_text = "Sucessfully updated the settings."
            messages.success(request, message_text)
        except:
            message_text = "Failed to update the settings. Please try again."
            messages.error(request, message_text)
    # return render(request, 'settings/settings.html')
    return redirect('settings')
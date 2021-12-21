from django.contrib import admin
from .models import *
# Register your models here.

class device_info_admin(admin.ModelAdmin):
    list_display = ['device_name', 'device_id', 'device_deptartment', 'device_location']
    list_filter = ['device_name', 'device_id', 'device_deptartment', 'device_location', 'device_emp_count']
    search_fields = ['device_name', 'device_id', 'device_deptartment', 'device_location',]
    list_per_page = 20
admin.site.register(deviceInfo, device_info_admin)

class commands_admin(admin.ModelAdmin):
    list_display = ['device_id', 'isExecuted', 'message', 'timestamp']
    list_filter = ['device_id', 'isExecuted', 'message']
    search_fields = ['device_id', 'isExecuted', 'message']
    list_per_page = 20
admin.site.register(commands, commands_admin)
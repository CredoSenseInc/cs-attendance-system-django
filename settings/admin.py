from django.contrib import admin
from .models import *
# Register your models here.

class settings_db_admin(admin.ModelAdmin):
    list_display = ['startTime', 'endTime', 'delayTime']
    # list_filter = ['emp_name', 'emp_id', 'emp_finger_id', 'emp_gender']
    # search_fields = ['emp_name', 'emp_id', 'emp_finger_id', 'emp_gender']
    list_per_page = 20
admin.site.register(settings_db, settings_db_admin)
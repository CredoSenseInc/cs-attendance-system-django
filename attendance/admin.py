from django.contrib import admin
from .models import *
# Register your models here.

class attendanceLog_admin(admin.ModelAdmin):
    list_display = ['emp_id', 'emp_present', 'date', 'emp_in_time', 'emp_out_time']
    list_filter = ['emp_id', 'emp_present', 'date', 'emp_in_time', 'emp_out_time']
    search_fields = ['emp_id', 'emp_present', 'date', 'emp_in_time', 'emp_out_time']
    list_per_page = 20
admin.site.register(attendanceLog, attendanceLog_admin)
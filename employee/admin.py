from django.contrib import admin
from .models import *
# Register your models here.

class employee_admin(admin.ModelAdmin):
    list_display = ['emp_name', 'emp_id', 'emp_finger_id', 'emp_gender']
    list_filter = ['emp_name', 'emp_id', 'emp_finger_id', 'emp_gender']
    search_fields = ['emp_name', 'emp_id', 'emp_finger_id', 'emp_gender']
    list_per_page = 20
admin.site.register(employee, employee_admin)
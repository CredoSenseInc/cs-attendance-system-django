from typing_extensions import Required
from django.db import models
import random

gender = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

salary_type = [
    ('M', 'Monthly'),
    ('H', 'Hourly'),
]

def generate_unique_fid():
    while True:
        f_id = random.randint(0, 128)
        if not employee.objects.filter(emp_finger_id=f_id).exists():
            break
    return f_id

class employee(models.Model):
    emp_name = models.CharField(max_length=255, blank=False, null=False)
    emp_contact_number = models.CharField(max_length=255, blank=False, null=False)
    emp_id = models.CharField(max_length=15, blank=False, null=False, unique = True)
    emp_finger_id = models.CharField(max_length=255, blank=False, null=False, unique = True, default=generate_unique_fid)
    emp_gender = models.CharField(max_length=255, blank=False, null=False, choices=gender)
    emp_designation = models.CharField(max_length=255, blank=False, null=False, default="")
    emp_dept = models.CharField(max_length=255, blank=False, null=False, default="")
    emp_salary_type = models.CharField(max_length=255, blank=False, null=False, choices=salary_type)
    emp_salary= models.CharField(max_length=255, blank=False, null=False, default="0")
    emp_overtime_per_hour = models.CharField(max_length=255, blank=False, null=False, default="0")


    def __str__(self):
            return f"{self.emp_id}"
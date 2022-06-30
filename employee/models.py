from operator import mod
from typing_extensions import Required
from django.db import models
import random
import time 

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
    timeout = time.time() + 30
    while True:
        print("Generating f_id")
        print(time.time())
        f_id = random.randint(1, 128)
        if not employee.objects.filter(emp_finger_id_1=f_id).exists():
            if not employee.objects.filter(emp_finger_id_2=f_id).exists():
                if not employee.objects.filter(emp_finger_id_3=f_id).exists():
                    if not employee.objects.filter(emp_finger_id_4=f_id).exists():
                        print("BLA")
                        break
        if time.time() > timeout:
            # f_id = 102122121839 # Error code failed to generate id
            return None
    print(f_id)
    return f_id

class employee(models.Model):
    emp_name = models.CharField(max_length=255, blank=False, null=False)
    emp_contact_number = models.CharField(max_length=255, blank=False, null=False)
    emp_id = models.CharField(max_length=15, blank=False, null=False, unique = True)
    email = models.EmailField(max_length=254, null= True, blank=True)

    emp_finger_id_1 = models.CharField(max_length=255, blank=False, null=False, unique = True, default=generate_unique_fid)
    emp_finger_id_2 = models.CharField(max_length=255, blank=True, null=False,  default="")
    emp_finger_id_3 = models.CharField(max_length=255, blank=True, null=False, default="")
    emp_finger_id_4 = models.CharField(max_length=255, blank=True, null=False,  default="")
    rfid_tag_number = models.CharField(max_length=255, blank=True, null=False,  default="")

    emp_gender = models.CharField(max_length=255, blank=False, null=False, choices=gender)
    emp_designation = models.CharField(max_length=255, blank=False, null=False, default="")
    emp_dept = models.CharField(max_length=255, blank=False, null=False, default="")
    emp_salary_type = models.CharField(max_length=255, blank=False, null=False, choices=salary_type)
    emp_salary= models.CharField(max_length=255, blank=False, null=False, default="0")
    emp_overtime_per_hour = models.CharField(max_length=255, blank=False, null=False, default="0")


    def __str__(self):
            return f"{self.emp_id}"
from typing_extensions import Required
from django.db import models

gender = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class employee(models.Model):
    emp_name = models.CharField(max_length=255, blank=False, null=False)
    emp_id = models.CharField(max_length=15, blank=False, null=False, unique = True)
    emp_finger_id = models.CharField(max_length=255, blank=False, null=False, unique = True)
    emp_gender = models.CharField(max_length=255, blank=False, null=False, choices=gender)
    emp_designation = models.CharField(max_length=255, blank=False, null=False, default="Software Engineer")
    emp_dept = models.CharField(max_length=255, blank=False, null=False, default="R&D")

    def __str__(self):
            return f"{self.emp_id}"
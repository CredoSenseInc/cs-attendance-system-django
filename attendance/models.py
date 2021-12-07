from django.db import models
from employee.models import employee

# Create your models here.
class attendanceLog(models.Model):
    #  = models.ForeignKey(employee, to_field='emp_id', on_delete=models.CASCADE, null=False, blank=False)
    emp_id = models.ForeignKey(employee, to_field='emp_id', null=False, blank=False, on_delete=models.CASCADE)
    emp_present = models.BooleanField(blank=False, null=False, default=False)
    date = models.DateField(blank=False, null=True)
    emp_in_time = models.TimeField(blank=False, null=True)
    emp_out_time = models.TimeField(blank=True, null=True)
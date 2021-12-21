import datetime
from django.core.checks import messages
from django.db import models
from django.conf import settings
import uuid

from django.db.models.expressions import F

# from api_esp.serializers import attendance_serializer
# bd_time = datetime.datetime.now(tz)

def generate_unique_id():
    while True:
        u_id = uuid.uuid4().hex[:6].upper()
        if not deviceInfo.objects.filter(device_id=u_id).exists():
            break
    return u_id

class deviceInfo(models.Model):
    device_name = models.CharField(max_length=255, blank=False, null=False)
    device_id = models.CharField(max_length=15, default=generate_unique_id, unique = True)
    device_deptartment = models.CharField(max_length=255, blank=False, null=False)
    device_location = models.CharField(max_length=255, blank=False, null=False)
    device_emp_count = models.IntegerField(default = 0, blank=False, null=False)

    def __str__(self):
            return f"{self.device_id}"

class commands(models.Model):
    device_id = models.ForeignKey(deviceInfo, to_field='device_id', null=False, blank=False, on_delete=models.CASCADE)
    isExecuted = models.BooleanField(null = False, blank = False, default= False)
    message = models.CharField(max_length=255, blank=False, null=False)
    scan_time = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)


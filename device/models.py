from contextlib import nullcontext
import datetime
from http.cookies import Morsel
from django.core.checks import messages
from django.db import models
from django.conf import settings
import uuid
from django.db.models.expressions import F
from importlib_metadata import version

# This portion is same as CS_MGT Device > models.py

# from api_esp.serializers import attendance_serializer
# bd_time = datetime.datetime.now(tz)

def generate_unique_id():
    while True:
        u_id = uuid.uuid4().hex[:6].upper()
        if not deviceInfo.objects.filter(device_id=u_id).exists():
            break
    return u_id

class deviceInfo(models.Model):
    device_name = models.CharField(max_length=255, blank=False, null=False, default="EMPTY")
    device_id = models.CharField(max_length=15, default=generate_unique_id, unique = True)
    device_deptartment = models.CharField(max_length=255, blank=True, null=True)
    device_location = models.CharField(max_length=255, blank=True, null=True)
    device_emp_count = models.IntegerField(default = 0, blank=True, null=True)
    firmware_version = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
            return f"{self.device_id}"


class firmware(models.Model):
    version = models.CharField(max_length=255, null=False, blank=False, default="0.0.1")
    url = models.CharField(max_length=255, null=False, blank=False, default="http://credosense.com/downloads")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    changelog = models.CharField(max_length=255, null=True, blank=True)


class commands(models.Model):
    device_id = models.ForeignKey(deviceInfo, to_field='device_id', null=False, blank=False, on_delete=models.CASCADE)
    isExecuted = models.BooleanField(null = False, blank = False, default= False)
    message = models.CharField(max_length=255, blank=False, null=False)
    server_message = models.CharField(max_length=255, blank=True, null=True, default="")
    scan_time = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)


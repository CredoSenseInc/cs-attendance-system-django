from django.db import models

# Create your models here.
class settings_db(models.Model):
    startTime = models.TimeField(null=False, blank=False, default="08:00:00")
    endTime = models.TimeField(null=False, blank=False, default="17:00:00")
    delayTime = models.TimeField(null=False, blank=False, default="08:15:59")
    offDay = models.TextField(blank=True, null=False)
    workDay = models.TextField(blank=True, null=False)
    week_saturday = models.BooleanField(blank=False, null=False, default=False)
    week_sunday = models.BooleanField(blank=False, null=False, default=False)
    week_monday = models.BooleanField(blank=False, null=False, default=False)
    week_tuesday = models.BooleanField(blank=False, null=False, default=False)
    week_wednesday = models.BooleanField(blank=False, null=False, default=False)
    week_thursday = models.BooleanField(blank=False, null=False, default=False)
    week_friday = models.BooleanField(blank=False, null=False, default=False)
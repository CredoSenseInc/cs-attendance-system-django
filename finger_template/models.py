from django.db import models

# Create your models here.
class template_info(models.Model):
    temp_id = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=20,blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    temp = models.CharField(max_length=4000,blank=True, null=True)
    flag = models.BooleanField( default=False)
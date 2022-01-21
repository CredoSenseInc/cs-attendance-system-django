from django.urls import path
from .views import *
urlpatterns = [
    path('', settings, name='settings'),
    path('update', update, name='update'),
    path('firmware-update', firmware_update, name='firmware_update'),
    ]
from django.urls import path
from .views import *
urlpatterns = [
    path('update', update_attendance, name='update_attendance'),
    path('view', download, name='download'),
    ]
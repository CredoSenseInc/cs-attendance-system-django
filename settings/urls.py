from django.urls import path
from .views import *
urlpatterns = [
    path('', settings, name='settings'),
    path('update', update, name='update'),
    ]
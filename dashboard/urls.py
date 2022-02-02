from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('view/', dashboard_view, name='dashboard_view'),
    ]
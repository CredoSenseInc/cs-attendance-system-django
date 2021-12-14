from django.urls import path
from .views import *
urlpatterns = [
    path('', employee_page, name='employee'),
    path('attendance-download', attendance_download, name='attendance-download'),
    path('attendance-name-search', attendance_download_search, name='attendance-download-search'),
    ]
from django.urls import path
from .views import *
urlpatterns = [
    path('', employee_page, name='employee'),
    path('add-emp', add_emp, name='add-emp'),
    path('update-emp', update_emp, name='update-emp'),
    path('scan-fingerprint/<int:fid>/<str:device>/', scan_fingerprint, name='scan-fingerprint'),
    path('attendance-log', attendance_download, name='attendance-download'),
    path('attendance-name-search', attendance_download_search, name='attendance-download-search'),
    ]
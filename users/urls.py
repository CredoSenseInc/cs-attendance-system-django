from django.urls import path
from .views import *
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('change-pass/', user_password_change, name='user_password_change'),
    ]
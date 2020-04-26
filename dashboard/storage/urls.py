from django.urls import path
from .views import *

app_name = 'storage'

urlpatterns = [
    path('devices', device_list, name='device_list'),
    path('devices/<device_id>', device_detail, name='device_detail'),
]
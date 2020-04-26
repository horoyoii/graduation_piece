from django.urls import path, re_path
from .views import *

app_name = 'app'

urlpatterns = [

    path('gateway/', gateway_list, name='gateway_list'),
    
    path('device/',  device_list, name='device_list'),
    
    path('device_service',  device_services, name='device_service'),
    path('device_log', device_logs, name='device_logs'),
    path('device_profile', device_profile, name='device_profile'),
    
    path('device/<device_id>', device_detail, name='device_detail'),
    path('device/register', device_register, name='device_register'),
    path('export/data', export_get_data, name='get_data'),

    # The home page
    path('', index, name='index'),
]

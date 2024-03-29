from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('result', DeviceCommandAgency.as_view(), name='result'),
    path('gateway', set_gateway, name='gateway_set'),
    path('device_service', get_device_service, name='get_ds'),
    path('device_profile', get_device_profile, name='get_pf'),
    path('device_name_list', get_device_name_list, name='get_nl'),
    path('cur_gateway', get_current_profile, name='cur_gt'),
    path('client', delete_client, name='delete_client')
]
"""gentella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include
from app.views import *

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # app/ -> Genetelella UI and resources
    url(r'^app/', include('app.urls')),
    url(r'^', include('app.urls')),

    path('gateways/', gateways, name='gateways'),

    path('devices/',  devices, name='devices'),
    path('devices/service',  device_services, name='device_service'),
    path('device/detail/<device_id>', device_detail, name='device_detail'),
    path('device/register', device_register, name='device_register'),
    path('devices/logs', device_logs, name='device_logs'),
    path('devices/profile', device_profile, name='device_profile'),

    path('export/data', export_get_data, name='get_data'),

    path('api/v1/result', DeviceCommandAgency.as_view(), name='result'),
    path('api/v1/gateway', set_gateway, name='gateway_set'),
    path('api/v1/device_service', get_device_service, name='get_ds'),
    path('api/v1/device_profile', get_device_profile, name='get_pf'),
    path('api/v1/cur_gateway', get_current_profile, name='cur_gt'),
    path('registeration/', include('registeration.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
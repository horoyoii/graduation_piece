from django.urls import path
from .views import *

app_name = 'registeration'

urlpatterns = [
    path('device_profile', device_profile, name='device_profile'),
    path('device', device_itself, name='device_itself'),
    #path('detail/<int:no>', HomeworkDetailView, name='homework_detail'),


]
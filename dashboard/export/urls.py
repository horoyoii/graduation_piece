from django.urls import path
from .views import *

app_name = 'export'

urlpatterns = [
    path('client', client_list, name='client_list'),
]
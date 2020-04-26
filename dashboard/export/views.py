from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
import json
import requests
import copy
from datetime import datetime
import time

def client_list(request):
    # gateway = cache.get(cache.get("cur_gateway"))
    # URL = 'http://'+gateway+':48082/api/v1/device'
    # response = requests.get(URL) 
    # print(response.status_code) 
    # res = json.loads(response.text) # type : list

    # device_list =[]
    # device_info = {}    

    # if res != None:
    #     for dev in res:
    #         device_info['id'] = dev['id'] 
    #         device_info['name'] = dev['name']
    #         device_info['os'] = dev['operatingState']
    #         device_info['labels'] = dev['labels']
    #         device_list.append(copy.deepcopy(device_info))
       
    return render(request, 'device.html')

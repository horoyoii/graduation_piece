from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
import json
import requests
import copy

# Create your views here.


def device_list(request):
    gateway = cache.get(cache.get("cur_gateway"))
    URL = 'http://'+gateway+':48082/api/v1/device'
    response = requests.get(URL) 
    print(response.status_code) 
    res = json.loads(response.text) # type : list

    device_list =[]
    device_info = {}    

    if res != None:
        for dev in res:
            device_info['id'] = dev['id'] 
            device_info['name'] = dev['name']
            device_info['os'] = dev['operatingState']
            device_info['labels'] = dev['labels']
            device_list.append(copy.deepcopy(device_info))
       
    return render(request, 'device.html', {'form': "hello world", 'devices':device_list})


def device_detail(request, device_id):
    """
    First 
    """
    gateway = cache.get(cache.get("cur_gateway"))
    URL = 'http://'+gateway+':48082/api/v1/device/'+device_id

    response = requests.get(URL) 
    res = json.loads(response.text) # type : list

    device_info = {}
    device_info['id'] = res['id'] 
    device_info['name'] = res['name']
    device_info['os'] = res['operatingState']
    device_info['labels'] = res['labels']


    # URL 
    cmd_list = res['commands']
    
    device_command_list =[]
    device_command_info = {}

    for dev in cmd_list:
        device_command_info['id'] = dev['id'] 
        device_command_info['name'] = dev['name']
        device_command_info['params'] = dev['put']['parameterNames']
        device_command_list.append(copy.deepcopy(device_command_info))
        print( device_command_info['params'])
    print(device_command_list)

    return render(request, 'device_detail.html', {'device_info':device_info, 'device_cmd_list':device_command_list})


    
import requests
import json
import copy
import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from datetime import datetime



def device_list(request):
    gateway = cache.get(cache.get("cur_gateway"))
    if gateway == None:
        return redirect('/registeration/gateway')

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
    First request to edgeX is for get the list of device resources.
    """
    gateway = cache.get(cache.get("cur_gateway"))
    if gateway == None:
        return redirect('/registeration/gateway')

    URL = 'http://'+gateway+':48082/api/v1/device/'+device_id

    response = requests.get(URL) 
    res = json.loads(response.text) # type : list

    device_info = {}
    device_info['id'] = res['id'] 
    device_info['name'] = res['name']
    device_info['os'] = res['operatingState']
    device_info['labels'] = res['labels']


    cmd_list = res['commands']
    
    resource_data_list =[]

    """
    Second request to edgeX is for getting the local data 
    """
    for dev in cmd_list:
        subURL = 'http://'+gateway+':48080/api/v1/reading/name/'+dev['put']['parameterNames'][0]+'/device/'+device_info['name']+'/10'

        response = requests.get(subURL) 
        res = json.loads(response.text) # type : list

        tmp_dic = {'name':dev['put']['parameterNames'][0]}

        tmp_list =[]
        for element in res:             # type : dict
            unixtime = element['created']

            t = datetime.fromtimestamp(
                unixtime / 1000
            ).strftime('%Y-%m-%d %H:%M:%S')

            ele = {'time':t, 'value' : element['value']}
            tmp_list.append(ele)

        tmp_dic['reading'] = tmp_list
        resource_data_list.append(copy.deepcopy(tmp_dic))

    return render(request, 'device_detail.html', {'device_info':device_info, 'resource_data':resource_data_list})


    

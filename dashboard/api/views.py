from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
import requests
import json
import copy

from django.core.cache import cache

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
import channels.layers
import datetime
from django.contrib.auth.models import User
from django.shortcuts import redirect



### Set Current Gateway
def set_gateway(request):

    cache.set("cur_gateway", request.GET.get('gt_name', None), timeout=None)

    return HttpResponse(status=200)   

def get_device_service(request):
    gateway = cache.get(cache.get("cur_gateway"))
    URL = 'http://'+gateway+':48081/api/v1/deviceservice'
    response = requests.get(URL) 
    res = json.loads(response.text) # type : list
    
    device_service_list =[]

    for dev in res:
        device_service_list.append(dev['name'])   
    rtn_dic = {"name":device_service_list}
    
    return JsonResponse(rtn_dic)



def get_device_profile(request):

    ### Make URL for EdgeX connection
    gateway = cache.get(cache.get("cur_gateway"))
    URL = 'http://'+gateway+':48081/api/v1/deviceprofile'

    ### Request to EdgeX 
    response = requests.get(URL) 
    res = json.loads(response.text)
    
    ### Parse Profile Info & Pass to Front 
    device_profile_list =[]


    for dev in res:
        device_profile_list.append(dev['name'])   
    
    rtn_dic = {"name":device_profile_list}
    

    return JsonResponse(rtn_dic)


def get_current_profile(request):
    gateway = cache.get(cache.get("cur_gateway"))
    return HttpResponse(gateway)



class DeviceCommandAgency(APIView):

    def get(self, request, format=None):

        ### Parse the params for sending request to EdgeX
        gateway = cache.get(cache.get("cur_gateway"))
        device_id = request.query_params.get('device_id', None)
        command_id = request.query_params.get('command_id', None)
        URL = 'http://'+gateway+':48082/api/v1/device/'+device_id+'/command/'+command_id
        
        ### Request to EdgeX 
        response = requests.get(URL)
        res = json.loads(response.text)
        ret_json= {}
        for n in res['readings']:
            ret_json[n['name']] = n['value']

        ### Response to Browser via ajax 
        return JsonResponse(ret_json)
    

    def post(self, request, format=None):

        ### Parse the params for sending request to EdgeX
        gateway = cache.get(cache.get("cur_gateway"))
        device_id = request.data['device_id']
        command_id = request.data['command_id']
        URL = 'http://'+gateway+':48082/api/v1/device/'+device_id+'/command/'+command_id        

        ### Parse Parameters
        body = request.data['body']
        print(body)
        ### Request(PUT) to EdgeX 
        headers = {'Content-Type': 'application/json'} 
        response = requests.put(URL, headers=headers, data=body)
        print(response)

        if response.status_code == 200:
            return Response()        
        else:
            return Response()

        return HttpResponse(status=200)    

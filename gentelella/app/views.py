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
from .forms import *
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import channels.layers
import datetime


def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def gateways(request):
    gateway = request.GET.get('gateway', None)
    if gateway != None:
        ### Test for redis
        cache.set("gateway1", gateway, timeout=None)
        print("cahced is set.....")
        print(gateway)
    else:
        print("none")
    
    return render(request, 'app/gateways.html', {'form': "hello world"})

@csrf_exempt
def export_get_data(request):
    print("export called")
    if request.method == "POST":
        j_data =request.body.decode('ascii')
        dict = json.loads(j_data)
        content = dict['id']
        
        dev_resource_name = dict['readings'][0]

        dev_res_name = dev_resource_name['name']
        dev_name = dev_resource_name['device']
        dev_value = dev_resource_name['value']
        print("==============================")

        # Disconnection 되었을 때 data 전달은 어떻게 되는가...?        
        channel_layer = channels.layers.get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "chat",
            {
            'type': 'chat_message',
                'message': "["+datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")+"] "+ dev_name +"    "+dev_res_name+"   "+dev_value
            }
        )

    return render(request, 'app/gateways.html', {'form': "hello world"})



def device_logs(request):
    return render(request, 'app/logs.html')



'''
'''
class DeviceCommandAgency(APIView):

    def get(self, request, format=None):

        ### Parse the params for sending request to EdgeX
        gateway = cache.get("gateway1") 
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
        gateway = cache.get("gateway1") 
        device_id = request.data['device_id']
        command_id = request.data['command_id']
        URL = 'http://'+gateway+':48082/api/v1/device/'+device_id+'/command/'+command_id        

        ### Parse Parameters
        body = request.data['body']
        print(body)
        print(type(body))



        ### Request(PUT) to EdgeX 
        headers = {'Content-Type': 'application/json'} 
        response = requests.put(URL, headers=headers, data=body)

        
        if response.status_code == 200:
            return Response()        
        else:
            return Response()


        return Response()        



def devices(request):
    
    gateway = cache.get("gateway1")
    URL = 'http://'+gateway+':48082/api/v1/device'
    response = requests.get(URL) 
    print(response.status_code) 
    res = json.loads(response.text) # type : list
    
    device_list =[]
    device_info = {}
    for dev in res:
        device_info['id'] = dev['id'] 
        device_info['name'] = dev['name']
        device_info['os'] = dev['operatingState']
        device_info['labels'] = dev['labels']
        device_list.append(copy.deepcopy(device_info))
       
    return render(request, 'app/device.html', {'form': "hello world", 'devices':device_list})



def device_services(request):

    gateway = cache.get("gateway1")
    URL = 'http://'+gateway+':48081/api/v1/deviceservice'
    response = requests.get(URL) 
    res = json.loads(response.text) # type : list
    
    device_service_list =[]
    device_service_info = {}
    for dev in res:
        device_service_info['id'] = dev['id'] 
        device_service_info['name'] = dev['name']
        device_service_info['os'] = dev['operatingState']
        device_service_info['labels'] = dev['labels']
        #device_info['labels'] = dev['']
 
        device_service_list.append(copy.deepcopy(device_service_info))
       
    return render(request, 'app/device_service.html', {'form': "hello world", 'devices':device_service_list})



def device_detail(request, device_id):
    gateway = cache.get("gateway1")
    URL = 'http://'+gateway+':48082/api/v1/device/'+device_id

    response = requests.get(URL) 
    res = json.loads(response.text) # type : list

    device_info = {}
    device_info['id'] = res['id'] 
    device_info['name'] = res['name']
    device_info['os'] = res['operatingState']
    device_info['labels'] = res['labels']

    cmd_list = res['commands']
    
    device_command_list =[]
    device_command_info = {}

    for dev in cmd_list:
        device_command_info['id'] = dev['id'] 
        device_command_info['name'] = dev['name']
        device_command_info['params'] = dev['put']['parameterNames']
        device_command_list.append(copy.deepcopy(device_command_info))
    print(device_command_list)

    return render(request, 'app/device_detail.html', {'device_info':device_info, 'device_cmd_list':device_command_list})


def device_register(request):
    if request.method == 'POST':
        rs = request.POST.copy()
        print(rs)
        print(rs.get('first-name'))


    return render(request, 'app/device_register_form.html')



def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


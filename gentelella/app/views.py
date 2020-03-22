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
from django.contrib.auth.models import User
from django.shortcuts import redirect


def index(request):
    print("index is called")
    if request.user.is_authenticated: # if user is not logged in 
        context = {}
        template = loader.get_template('app/index.html')
        return HttpResponse(template.render(context, request))
    else:
        print("Login plz")
        return redirect('/accounts/login')



### Show all Gateway from Redis 
def gateways(request):

    gateway = request.GET.get('gateway', None)

    ### Get All registered gateway info In redis
    gt_list = cache.keys("gateway*")
    gt_dic = {}

    for key in gt_list:
        gt_dic[key] = cache.get(key)

    ### Register New Gateway info in Redis
    if gateway != None:
        gt_num = cache.get("num")
        if gt_num == None:
            gt_num = 0 

        gt_num = gt_num + 1
        cache.set("gateway_"+str(gt_num), gateway, timeout=None)
        cache.set("num", gt_num, timeout=None)
        
    else:
        print("none")
    
    return render(request, 'app/gateways.html', {'gt_dic':gt_dic})


### Set Current Gateway
def set_gateway(request):

    cache.set("cur_gateway", request.GET.get('gt_name', None), timeout=None)

    return HttpResponse(status=200)   




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



def device_profile(request):

    ### Make URL for EdgeX connection
    gateway = cache.get(cache.get("cur_gateway"))
    URL = 'http://'+gateway+':48081/api/v1/deviceprofile'

    ### Request to EdgeX 
    response = requests.get(URL) 
    print(response.status_code) 
    res = json.loads(response.text) # type : list
    
    ### Parse Profile Info & Pass to Front 
    device_profile_list =[]
    device_profile_info = {}
    for dev in res:
        device_profile_info['id'] = dev['id'] 
        device_profile_info['name'] = dev['name']
        device_profile_info['model'] = dev['model']
        device_profile_info['manufacturer'] = dev['manufacturer']
        device_profile_info['labels'] = dev['labels']
        device_profile_info['description'] = dev['description']
        device_profile_list.append(copy.deepcopy(device_profile_info))

    print(device_profile_list)

    return render(request, 'app/device_profile.html', {'device_profile_list':device_profile_list})



'''
'''
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
        print(type(body))



        ### Request(PUT) to EdgeX 
        headers = {'Content-Type': 'application/json'} 
        response = requests.put(URL, headers=headers, data=body)

        
        if response.status_code == 200:
            return Response()        
        else:
            return Response()


        return HttpResponse(status=200)    



def devices(request):
    
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
       
    return render(request, 'app/device.html', {'form': "hello world", 'devices':device_list})



def device_services(request):

    gateway = cache.get(cache.get("cur_gateway"))
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
       
    return render(request, 'app/device_service.html', {'devices':device_service_list})



def device_detail(request, device_id):
    gateway = cache.get(cache.get("cur_gateway"))
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

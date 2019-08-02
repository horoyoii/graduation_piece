from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
import requests
import json
import copy

from django.core.cache import cache

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



'''
'''
def result(request):
    
    ### Parse the params for sending request to EdgeX
    gateway = cache.get("gateway1") 
    device_id = request.GET.get('device_id', None)
    command_id = request.GET.get('command_id', None)
    URL = 'http://'+geteway+':48082/api/v1/device/'+device_id+'/command/'+command_id
    
    ### Request to EdgeX 
    response = requests.get(URL)
    res = json.loads(response.text)
    ret_json= {}
    for n in res['readings']:
        ret_json[n['name']] = n['value']
        print(n['name'])
        print(n['value'])


    ### Response to Browser via ajax 
    return JsonResponse(ret_json)




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
        device_command_list.append(copy.deepcopy(device_command_info))
    print(device_command_list)

    return render(request, 'app/device_detail.html', {'device_info':device_info, 'device_cmd_list':device_command_list})



def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


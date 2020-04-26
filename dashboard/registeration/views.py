import requests
import json
import copy
import os

from django.http import HttpResponseRedirect,HttpResponse
from django.core.cache import cache
from django.shortcuts import render

from .forms import *


def gateway(request):

    gateway = request.GET.get('gateway', None)

    ### Get All registered gateway info In redis
    print(cache.keys("gateway*"))

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
    
    return render(request, 'gateways.html')

def client(request):
    if request.method == 'POST':
        print(request.POST['device_profile_list'])
        print(request.POST['device_service_list'])

        ### Parse the params for sending request to EdgeX
        gateway = cache.get(cache.get("cur_gateway")) 
#        URL = 'http://'+gateway+':48081/api/v1/device'

        ### Parse Parameters

        body = {
            "name": request.POST['name'],
            "description": request.POST['Description'],
            "adminState": request.POST['adminState'],
            "operatingState": request.POST['operatingState'],
            "protocols": {
                request.POST['Protocol']:{
                    "Address": request.POST['Address'],
                    "Port": request.POST['Port'],
                    "UnitID": request.POST['UnitID']
                }
            },
            "service":{
                "name": request.POST['device_service_list'],
                "adminState":"unlocked",
                "operatingState":"enabled",
                "addressable":{
                    "name": request.POST['device_service_list']
                }
            },
            "profile":{
                "name": request.POST['device_profile_list']
            }
        }

        ### Set autoEvent if any.
        eventList = []
        field_num = int(request.POST['field_num'])
        print(field_num)

        for idx in range(1, field_num+1):
            t_dic = {}
            t_dic["frequency"] = request.POST['time'+str(idx)]+"ms"
            t_dic["onChange"] = False
            t_dic["resource"] = request.POST['resource'+str(idx)]
            eventList.append(copy.deepcopy(t_dic))

        if field_num:
            body["autoEvents"] = eventList


        ### Make python Dic to Json format
        json_body = json.dumps(body)
        print(json_body)

        ### Request(POST@@) to EdgeX 
        headers = {'Content-Type': 'application/json'} 
        response = requests.post(URL, headers=headers, data=json_body)

        
        if response.status_code == 200:
            return HttpResponseRedirect('/registeration/device')        
        else:
            return HttpResponseRedirect('/registeration/device')

    return render(request, 'client_upload.html')


def device_profile(request):
    if request.method == 'POST':
        form = ProfileFormModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            ### Get File name
            f_name = request.FILES['device_profile_file'].name
            #print(f_name)


            ### Get File from local Dir
            cwd = os.getcwd()
            file_path = os.path.join(cwd, 'uploads/'+f_name)
            #print(file_path)


            ### Sent the file to EdgeX
            gateway = cache.get(cache.get("cur_gateway"))
            URL = 'http://'+gateway+':48081/api/v1/deviceprofile/uploadfile'
            #print(URL)

            ### Request to EdgeX 
            files = {'file': open(file_path, 'rb')}

            r = requests.post(URL, files=files)
            print(r)


            return HttpResponseRedirect('/registeration/device_profile')
    else:
        form = ProfileFormModel()
    return render(request, 'device_profile.html', {'form': form})




def device_itself(request):
    if request.method == 'POST':
        print(request.POST['device_profile_list'])
        print(request.POST['device_service_list'])

        ### Parse the params for sending request to EdgeX
        gateway = cache.get(cache.get("cur_gateway")) 
        URL = 'http://'+gateway+':48081/api/v1/device'

        ### Parse Parameters

        body = {
            "name": request.POST['name'],
            "description": request.POST['Description'],
            "adminState": request.POST['adminState'],
            "operatingState": request.POST['operatingState'],
            "protocols": {
                request.POST['Protocol']:{
                    "Address": request.POST['Address'],
                    "Port": request.POST['Port'],
                    "UnitID": request.POST['UnitID']
                }
            },
            "service":{
                "name": request.POST['device_service_list'],
                "adminState":"unlocked",
                "operatingState":"enabled",
                "addressable":{
                    "name": request.POST['device_service_list']
                }
            },
            "profile":{
                "name": request.POST['device_profile_list']
            }
        }

        ### Set autoEvent if any.
        eventList = []
        field_num = int(request.POST['field_num'])
        print(field_num)

        for idx in range(1, field_num+1):
            t_dic = {}
            t_dic["frequency"] = request.POST['time'+str(idx)]+"ms"
            t_dic["onChange"] = False
            t_dic["resource"] = request.POST['resource'+str(idx)]
            eventList.append(copy.deepcopy(t_dic))

        if field_num:
            body["autoEvents"] = eventList


        ### Make python Dic to Json format
        json_body = json.dumps(body)
        print(json_body)

        ### Request(POST@@) to EdgeX 
        headers = {'Content-Type': 'application/json'} 
        response = requests.post(URL, headers=headers, data=json_body)

        print("RESPONE:::: ",response.status_code)
        print("RESPONE:::: ",response.content)

        
        if response.status_code == 200:
            return HttpResponseRedirect('/registeration/device')        
        else:
            return HttpResponseRedirect('/registeration/device')



    else:
        print("OKKKK")
    
    return render(request, 'device_upload.html')
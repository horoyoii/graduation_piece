from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect,HttpResponse
import requests
from django.core.cache import cache
import os
import json
# Create your views here.


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
        print("POST OKKKK")
        print(request.POST['name'])

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
                "name": request.POST['Device_Service'],
                "adminState":"unlocked",
                "operatingState":"enabled",
                "addressable":{
                    "name": request.POST['Device_Service']
                }
            },
            "profile":{
                "name": request.POST['Device_Profile']
            }
        }

        ### Make python Dic to Json format
        json_body = json.dumps(body)

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
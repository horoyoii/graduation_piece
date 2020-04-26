import requests
import json
import copy

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.cache import cache


def get_client_list(request):
    gateway = cache.get(cache.get("cur_gateway"))
    URL = 'http://'+gateway+':48071/api/v1/registration'
    response = requests.get(URL) 

    print(response.status_code) 
    client_list = json.loads(response.text) # type : list

    ret_list =[]
    ret_info = {}    

    if client_list != None:
        for client in client_list: 
            ret_info['id'] = client['id']
            ret_info['name'] = client['name']
            ret_info['destination'] = client['destination']
            
            addr = client['addressable']
            ret_info['protocol'] = addr['protocol']
            if "address" in addr:
                ret_info['address']  = addr['address']+":"+str(addr['port'])
            if "path" in addr:
                ret_info['address'] += addr['path']

            filter = client['filter']
            if "deviceIdentifiers" in filter:
                ret_info['interests'] = filter['deviceIdentifiers']

            ret_list.append(copy.deepcopy(ret_info))
    
    print(ret_list)
    return render(request, 'clients.html', {'client_list':ret_list})

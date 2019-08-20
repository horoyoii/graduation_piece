from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect,HttpResponse
import requests
from django.core.cache import cache
import os
# Create your views here.


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
            gateway = cache.get("gateway1") 
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

    return None
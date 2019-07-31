from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import requests
import json

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def devices(request):
    URL = 'http://115.145.226.221:48082/api/v1/device'
    response = requests.get(URL) 
    print(response.status_code) 
    kk = json.loads(response.text)
    print(kk[1]["id"])

    #print(y["data"])




    return render(request, 'app/tables_dynamic.html', {'form': "hello world"})





def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


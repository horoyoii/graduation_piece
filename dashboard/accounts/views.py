from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.

def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user is None:
            return redirect('/accounts/login')
        else:
            ### Login Success
            auth_login(request, user)    
            return redirect('/app')

    ### GET method 
    else:
        return render(request, 'app/login.html') 

def logout(request):

    auth_logout(request)

    return redirect('/accounts/login')
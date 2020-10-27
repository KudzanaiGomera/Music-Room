from django.shortcuts import render,redirect
from decouple import config
from django.contrib.auth.models import User
from Profile.models import User_Profile
from .forms import LoginForm
from django.contrib.auth.models import User,auth
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from decouple import config

import requests

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = strip_tags(form.cleaned_data['username'])
            password = strip_tags(form.cleaned_data['password'])
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                print("Temp user created!")
                return render(request,"home.html")
            else:     
                form = LoginForm()
                message = "Username/Password is not valid.Otherwise check email to activate account"
                # UID = config('UID')
                # SECRET = config('SECRET')
                # token = Token.objects.create(
                    # UID,SECRET,site:"https://api.intra.42.fr")
                # print("Token", JSON.stringify(token))
                context={"form":form,"message":message}
                return render(request,"login.html",context)
    else:
        form = LoginForm()
        return render(request,"login.html",{"form":form})

@login_required(login_url='/')       
def home_view(request,*args, **kwargs):
        return render(request,"home.html")

@login_required(login_url='/')       
def logout_view(request):
        auth.logout(request)
        return redirect("/")



        
# Create your views here.

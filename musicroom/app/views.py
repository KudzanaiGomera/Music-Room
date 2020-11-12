from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import connections
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import AccountForm, UserUpdateForm, ProfileForm
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.dates import YearArchiveView
from django.core.files.storage import FileSystemStorage
import mysql.connector
import bcrypt
import re, sys
import requests
import os
from .models import Playlist
from django.core.serializers import serialize

sys.setrecursionlimit(1500)

# Create your views here.

def index(request):

    return render(request, 'index.html')


def login2(request):
    #check if username and password POST requests exits (user submitted form)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,email=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "incorrect Email or Password...")
    return render(request, 'login.html')

def register(request):
    form = AccountForm()
   
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            user  = form.cleaned_data.get('email')

            messages.success(request, 'Account successfully created for ' + user)
            return redirect('login2')
        
    context = {'form':form}   
    return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login2')

def music(request):
     # playlist = Playlist.objects.all()
    all_users = User.objects.all()
    all_users = all_users.exclude(username=request.user.username)#remove this if issues
    public_list = Playlist.objects.filter(playlist_status='Public')
    private_list = Playlist.objects.filter(playlist_status='Private')
    for k in private_list:
        Found = ""
        user_array=k.playlist_members.split(',')
        for j in user_array:
            if(j==request.user.username):
                Found = "Match"
        if (Found != "Match"):
            private_list=private_list.exclude(playlist_name=k.playlist_name)
    json_user = serialize('json',all_users,fields=['username'])
    context ={
        "public_list" : public_list,
        "private_list" : private_list,
        "all_users":all_users,
       "json_user":json_user,
    }
    return render(request,"music.html",context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Account successfully Updated for ')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


# def code_check(request): #Playlist
    # code_deezer=request.GET.get('code')
    # request.session['store_var']=code_deezer
    # print("code api: ", code_deezer)
    # if (code_deezer):
        # print("Code_playlist_view",code_deezer)
        # user_get=requests.get('https://connect.deezer.com/oauth/access_token.php?app_id=443742&secret=9c0af8b323f6d6ab1632e81319a6d0f5&code='+code_deezer)
        # link=user_get.text
        # print("Access token_playlist_view:",link.strip('access_token='))
        # details=requests.get('https://api.deezer.com/user/me?access_token='+link.strip('access_token='))
        # request.session['access_token']=link.strip('access_token=')
        # print("Session access token", request.session.get('access_token'))
    # deezer_username=details.json()['firstname']
    # deezer_email=details.json()['email']
    # User.objects.get_or_create(username=deezer_username,email=deezer_email)
    # user = User.objects.get(email=deezer_email)
    # login(request,user,backend='django.contrib.auth.backends.ModelBackend')
    # user.is_active=True
    
    #delete_track(request,'8266792942')
    # create_playlist(request)
    # add_track(request)
    #delete_playlist(request,'8266792942')
    # return redirect("/playlist_view")

# def playlist_view(request):
    # playlist = Playlist.objects.all()
    # all_users = User.objects.all()
    # all_users = all_users.exclude(username=request.user.username)#remove this if issues
    # public_list = Playlist.objects.filter(playlist_status='Public')
    # private_list = Playlist.objects.filter(playlist_status='Private')
    # for k in private_list:
        # Found = ""
        # user_array=k.playlist_members.split(',')
        # for j in user_array:
            # if(j==request.user.username):
                # Found = "Match"
        # if (Found != "Match"):
            # private_list=private_list.exclude(playlist_name=k.playlist_name)
    # json_user = serialize('json',all_users,fields=['username'])
    # context ={
        # "public_list" : public_list,
        # "private_list" : private_list,
        # "all_users":all_users,
    #    "json_user":json_user,
    # }
    # list_playlist(request)
    # return render(request,"playlist.html",context)
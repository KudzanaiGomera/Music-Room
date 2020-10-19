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

    return render(request, 'music.html')

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
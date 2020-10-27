from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("User status",user)
        if user is not None and user.is_active:
            login(request, user)
            return render(request,"home.html")  
        else:
            message = "Username/Password is not valid.Otherwise check email to activate account"
            return render(request,"login.html",{'message':message})
    return render(request,"login.html")

# Create your views here.

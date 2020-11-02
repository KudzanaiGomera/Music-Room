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
import datetime
from Pages.models import Song

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

# @login_required(login_url='/')       
def search_view(request):
    # print('Deezer_token',request.session.get('access_token'))
    if request.method == 'POST':
        name = request.POST['search_artist']
        print(name)
        search_url = 'https://api.deezer.com/search?q=' + str(name)+'&limit=10'
        json_response = requests.get(search_url).json()
        info = json_response['data']
        # print("Results",search_url)
        for k in info:
            time_value =datetime.timedelta(seconds=k['duration'])
            print("The type is : ",type(time_value))
            Song.objects.get_or_create(
                track_id=k['id'],
                artist_name = k['artist']['name'],
                song_title = k['title'],
                track_preview=k['preview'],
                artist_image= k['album']['cover_medium'],
                convert_time=time_value,
            )
            # print("Song Title", song_title)
            # print("Song Title", song_title)
            # print("Song Title", song_title)
            # artist = requests.get(search_url).json()
            # song_title = k
            # print("K :",k)
            # artist_name = artist['data'][k]['artist']['name']
            # artist_image= artist['data'][k]['album']['cover_medium']
            # print("Artist name: ",artist_name)
            # print('Track' ,track_id)
            # print("Song title: ",song_title)
            # print("Artist", artist_name)
            # print("Artist_image: ", artist_image)
            # print('Artist preview',track_preview)
            # print('Duration',convert_time)
            # print('------')
            # context = { 
                # 'song_title':song_title,
                # 'artist_name': artist_name,
                # 'artist_image':artist_image,
                # 'track_preview':track_preview,
                # 'convert_time':convert_time,
            # }
    return render(request,"search.html")        

@login_required(login_url='/')       
def logout_view(request):
        auth.logout(request)
        return redirect("/")



        
# Create your views here.

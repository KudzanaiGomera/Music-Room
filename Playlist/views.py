from django.shortcuts import render,redirect
from Profile.models import Playlist
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.serializers import serialize
import json
import requests
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    return render(request,"index.html",{})

def playlist_name(request,playlist_name):#old code
    private_list = Playlist.objects.filter(playlist_status='Private').filter(playlist_name=playlist_name)
    public_list = Playlist.objects.filter(playlist_status='Public').filter(playlist_name=playlist_name)
    context={
        "playlist_name":playlist_name,
        "private_list":private_list,
        "public_list":public_list,

    }
    return(render(request,"playlist_name.html",context))
def api_delete_playlist(request,code):#working
    # playlist_id = '8266367462'
    results=requests.delete('https://api.deezer.com/playlist/'+str(code)+'&access_token='+request.session.get('access_token'))
    print("delete_response",results.text)

def api_create_playlist(request,playlist_name): #working
    results=requests.post('https://api.deezer.com/user/me/playlists?title='+playlist_name+'&collaborative='+str(False)+'&access_token='+request.session.get('access_token'))
    return results.json()['id']

def list_playlist(request):
    session_access_token = request.session.get('access_token')
    results=requests.get('https://api.deezer.com/user/me/playlists?access_token='+session_access_token)
    print(results.json())


def code_check(request): #Playlist
    code_deezer=request.GET.get('code')
    request.session['store_var']=code_deezer
    print("code api: ", code_deezer)
    if (code_deezer):
        print("Code_playlist_view",code_deezer)
        user_get=requests.get('https://connect.deezer.com/oauth/access_token.php?app_id=440262&secret=e7869287d15cf287412ee1bf64c0cc84&code='+code_deezer)
        link=user_get.text
        print("Access token_playlist_view:",link.strip('access_token='))
        details=requests.get('https://api.deezer.com/user/me?access_token='+link.strip('access_token='))
        request.session['access_token']=link.strip('access_token=')
        print("Session access token", request.session.get('access_token'))
    deezer_username=details.json()['firstname']
    deezer_email=details.json()['email']
    User.objects.get_or_create(username=deezer_username,email=deezer_email)
    user = User.objects.get(username=deezer_username)
    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
    user.is_active=True
    
    #delete_track(request,'8266792942')
    # create_playlist(request)
    # add_track(request)
    #delete_playlist(request,'8266792942')
    return redirect("/playlist_view")

def playlist_view(request):
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
    list_playlist(request)
    return render(request,"playlist.html",context)
def playlist_delete(request): # old code
    if request.method == 'POST':
        get_playlist_id= Playlist.objects.filter(pk=request.POST['button_id']).values('playlist_id')
        for k in get_playlist_id:
            api_delete_playlist(request,k['playlist_id'])
        Playlist.objects.filter(pk=request.POST['button_id']).delete()
    return HttpResponse("Playlist deleted")

def playlist_edit(request): #old code
    print("im in edit")
    id_value=Playlist.objects.get(pk=request.POST['button_id'])
    if request.method == 'POST':
        # form =Playlist(request.POST,instance=id_value)
        print("Edit id :" , id_value)
    return render(request,"playlist.html")

def get_host(request): #playlist
    get_host= Playlist.objects.filter(id=request.POST['id'])
    for k in get_host:
        host=k.playlist_owner
    return HttpResponse(host)

def playlist_add(request): #old code
    if request.method == 'POST':
        print("Here the value: ",request.POST['check_1'])
        if request.POST['check_1'] == 'false':
            value = "Public"
            print("This is public")
        else:
            value = "Private"
            print("This is private")
        # api_create_playlist(request,request.POST['play_name'])
        record = Playlist(playlist_name=request.POST['play_name'],
        playlist_owner=request.user,
        playlist_members = request.POST['user_string'],
        playlist_status = value,
        playlist_id = api_create_playlist(request,request.POST['play_name']),
        )
    if Playlist.objects.filter(playlist_name=request.POST['play_name']).filter(playlist_owner=request.user).count() < 1:
        record.save()
    return HttpResponse(record.id)
    

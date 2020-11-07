from django.shortcuts import render,redirect
from app.models import Playlist
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.serializers import serialize
import json
import requests
import datetime
from django.contrib.auth import authenticate, login

# Create your views here.

def code_check(request): #Deezer auth + user create
    code_deezer=request.GET.get('code')
    request.session['store_var']=code_deezer
    print("code api: ", code_deezer)
    if (code_deezer):
        print("Code_playlist_view",code_deezer)
        user_get=requests.get('https://connect.deezer.com/oauth/access_token.php?app_id=443742&secret=9c0af8b323f6d6ab1632e81319a6d0f5&code='+code_deezer)
        link=user_get.text
        print("Access token_playlist_view:",link.strip('access_token='))
        details=requests.get('https://api.deezer.com/user/me?access_token='+link.strip('access_token='))
        request.session['access_token']=link.strip('access_token=')
        print("Session access token", request.session.get('access_token'))
    deezer_username=details.json()['firstname']
    deezer_email=details.json()['email']
    User.objects.get_or_create(username=deezer_username,email=deezer_email)
    user = User.objects.get(email=deezer_email)
    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
    user.is_active=True
    
    #delete_track(request,'8266792942')
    # create_playlist(request)
    # add_track(request)
    #delete_playlist(request,'8266792942')
    return redirect("/playlist_view")


def playlist_view(request):#Playlist view template
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
    # list_playlist(request)
    
    return render(request,"playlist.html",context)
def get_host(request): #playlist
    get_host= Playlist.objects.filter(id=request.POST['id'])
    for k in get_host:
        host=k.playlist_owner
    return HttpResponse(host)

def playlist_name(request,playlist_name):#Get playlist name + search_results
    artist_value = []
    fetch_playlist_track_api=[]
    if request.method == 'POST' and request.POST['search_artist']:
        name = request.POST['search_artist']
        print("Searching for user :",name)
        search_url2 = 'https://api.deezer.com/search/track?q=' + str(name)+'&limit=10'
        json_response = requests.get(search_url2).json()
        info = json_response['data']
        for k in info:
            time_value =datetime.timedelta(seconds=k['duration'])
            value={'artist_id': k['id'],'artist_name':k['artist']['name'],'title': k['title'],'preview_link':k['preview'],'album_art':k['album']['cover_medium'], 'duration':time_value,'album_title':k['album']['title']}
            artist_value.append(value)


    private_list = Playlist.objects.filter(playlist_status='Private').filter(playlist_name=playlist_name)
    public_list = Playlist.objects.filter(playlist_status='Public').filter(playlist_name=playlist_name)
    get_pk = Playlist.objects.filter(playlist_name=playlist_name).values('playlist_id')
    for j in get_pk:
        playlist_id = j['playlist_id']
    get_host = Playlist.objects.filter(playlist_id=playlist_id).values('playlist_owner')#get host of playlist
    for m in get_host:
        playlist_host=m['playlist_owner']
    get_status= Playlist.objects.filter(playlist_id=playlist_id).values('playlist_status')#get playlist private or public status
    for q in get_status:
        playlist_status=q['playlist_status']

    # fetch songs from playlist  when  pages refresh from API
    songs_on_playlist_api= 'https://api.deezer.com/playlist/'+str(playlist_id)+'/tracks'+'&access_token='+request.session.get('access_token')
    json_response = requests.get(songs_on_playlist_api).json()
    info2 = json_response['data']
    for k in info2:
        time_value =datetime.timedelta(seconds=k['duration'])
        value= { 'artist_id':k['id'] ,'title':k['title'] ,'album_title':k['album']['title'],'artist_name':k['artist']['name'],'duration':time_value,'preview_link':k['preview'],'album_art':k['album']['cover_medium']}
        fetch_playlist_track_api.append(value)
    current_playlist=fetch_playlist_track_api
    context={
        "playlist_name":playlist_name,
        "private_list":private_list,
        "public_list":public_list,
        "artist_value":artist_value,
        "playlist_id":playlist_id,
        "current_playlist":current_playlist,
        "playlist_host":playlist_host,
        "playlist_status":playlist_status,
    }
    return(render(request,"playlist_name.html",context))

def playlist_add(request):# Add playlist in database
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

def playlist_delete(request): #Delete  playlist in database
    if request.method == 'POST':
        get_playlist_id= Playlist.objects.filter(pk=request.POST['button_id']).values('playlist_id')
        for k in get_playlist_id:
            api_delete_playlist(request,k['playlist_id'])
        Playlist.objects.filter(pk=request.POST['button_id']).delete()
    return HttpResponse("Playlist deleted")

def api_create_playlist(request,playlist_name):#API request to create playlist
    results=requests.post('https://api.deezer.com/user/me/playlists?title='+playlist_name+'&collaborative='+str(False)+'&access_token='+request.session.get('access_token'))
    print("Playlist id :" ,results.json()['id'])
    # api_add_song(request,results.json()['id'])
    # api_delete_song(request,results.json()['id'])
    
    return results.json()['id']

def api_delete_playlist(request,code):#API request to delete song from playlist
    # playlist_id = '8266367462'
    results=requests.delete('https://api.deezer.com/playlist/'+str(code)+'&access_token='+request.session.get('access_token'))
    print("delete_response",results.text)

def api_delete_song(request):#API request to delete song from playlist 
    if request.method == 'POST':
        results = requests.delete('https://api.deezer.com/playlist/'+str(request.POST['playlist_code'])+'/tracks'+'?songs='+request.POST['track_id']+'&access_token='+request.session.get('access_token'))
        print("Song deleted",results.text)
        print("Song deleted from playlist : ", request.POST['playlist_code'])
        return HttpResponse("Song deleted")

def api_add_song(request): #API request to add song from playlist
    if request.method == 'POST':
        results = requests.post('https://api.deezer.com/playlist/'+str(request.POST['playlist_code'])+'/tracks'+'?songs='+request.POST['track_id']+'&access_token='+request.session.get('access_token'))
        print("Song added",results.text)
        print("Song added to playlist", request.POST['playlist_code'])
        return HttpResponse("Song Added")

def list_playlist(request):#list current playlist
    session_access_token = request.session.get('access_token')
    results=requests.get('https://api.deezer.com/user/me/playlists?access_token='+session_access_token)
    print(results.json())

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from app.models import Playlist
from asgiref.sync import sync_to_async
class Playlist_view_consumer(AsyncWebsocketConsumer):
    # async def Playlist():
        # print("All profile data:",Playlist.objects.all())

    async def connect(self):
        self.playlist_view='Playlist_view'
        await self.channel_layer.group_add(
            self.playlist_view,
            self.channel_name
        )
        await self.accept()
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        playlist_name=text_data_json['playlist_name']
        delete_playlist=text_data_json['delete_playlist']
        playlist_pk=text_data_json['playlist_pk']
        status=text_data_json['status']
        # Playlist()

        await self.channel_layer.group_send(
            self.playlist_view,
            {
                'type': 'playlist_name_build',
                'playlist_name':playlist_name,
                'delete_playlist':delete_playlist,
                 'playlist_pk':playlist_pk,
                 'status':status,
            }
        )
    async def playlist_name_build(self,event):
        playlist_name= event['playlist_name'],
        delete_playlist = event['delete_playlist'],
        playlist_pk=event['playlist_pk'],
        status=event['status'],

        await self.send(text_data=json.dumps({
            'playlist_name':playlist_name,
            'delete_playlist':delete_playlist,
            'playlist_pk':playlist_pk,
            'status':status,
        }))
    

class PlaylistConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.playlist_name = self.scope['url_route']['kwargs']['playlist_name']
        self.playlist_list_name = 'playlist_%s' % self.playlist_name
        
        await self.channel_layer.group_add(
            self.playlist_list_name,
            self.channel_name
        )
        await self.accept()



    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.playlist_list_name,
            self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'],
        user_name = text_data_json['user_name'],
        delete_song = text_data_json['delete_song'],

        await self.channel_layer.group_send(
            self.playlist_list_name,
            {
                'type':'playlist_build',
                'message': message,
                'user_name':user_name,
                'delete_song':delete_song,
            }
        )
    async def playlist_build(self,event):
        message= event['message'],
        user_name= event['user_name'],
        delete_song= event['delete_song'],
        

        await self.send(text_data=json.dumps({
            'message':message,
            'user_name': user_name,
            'delete_song':delete_song,
        }))


    # pass
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/playlist/(?P<playlist_name>\w+)/$',consumers.PlaylistConsumer),
    re_path(r'ws/playlist_view/$',consumers.Playlist_view_consumer),
]
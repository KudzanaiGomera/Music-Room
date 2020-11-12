from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/playlist/(?P<playlist_name>\w+)/$',consumers.PlaylistConsumer.as_asgi()),
    re_path(r'ws/playlist_view/$',consumers.Playlist_view_consumer.as_asgi()),
]
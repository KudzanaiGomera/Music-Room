from django.urls import path
from . import views

urlpatterns = [
    path('<str:playlist_name>/',views.playlist_name,name='playlist_name'),
]
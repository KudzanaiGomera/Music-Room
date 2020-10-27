from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('<str:playlist_name>/',views.playlist_name,name='playlist_name'),
]
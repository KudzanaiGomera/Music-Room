"""Hypertube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Pages.views import home_view,login_view,logout_view
from Playlist.views import playlist_view,playlist_add,playlist_delete,playlist_edit,code_check,get_host
urlpatterns = [
    path('', login_view, name='login'),
    path('home/',home_view,name='home'),
    path('code_check/',code_check,name='code_check'),
    path('logout/',logout_view,name='logout'),
    path('playlist_view/',playlist_view,name='playlist_view'),
    path('playlist_add/',playlist_add,name='playlist_add'),
    path('playlist/', include('Playlist.urls')),
    path('playlist_delete/',playlist_delete,name='playlist_delete'),
    path('get_host/',get_host,name='playlist_delete'),
    path('playlist_edit/',playlist_edit,name='playlist_edit'),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

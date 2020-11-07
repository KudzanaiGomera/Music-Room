from django.urls import path, NoReverseMatch
from django.conf import settings

from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views 
from Playlist.views import code_check, playlist_view,playlist_add,playlist_delete,api_add_song,api_delete_song


urlpatterns = [
    path('', views.index, name='index'),
    # Playlist code start
    path('code_check/', code_check,name='code_check'),
    path('playlist_view/', playlist_view,name='playlist_view'),
    path('playlist/', include('Playlist.urls')),
    path('playlist_add/',playlist_add,name='playlist_add'),
    path('playlist_delete/',playlist_delete,name='playlist_delete'),
    path('api_add_song/',api_add_song,name='api_add_song'),
    path('api_delete_song/',api_delete_song,name='api_delete_song'),
    
    # Playlist code end
    path('login.html', views.login2, name='login2'),
    path('register.html', views.register, name='register'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('music.html', views.music, name='music'),
    path('profile.html', views.profile, name='profile'),

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
        name="password_reset_confirm"),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),

    path('oauth/', include('social_django.urls',namespace='social')),
]
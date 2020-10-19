from django.urls import path, NoReverseMatch
from django.conf import settings

from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
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
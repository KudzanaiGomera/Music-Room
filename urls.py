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

from Pages.views import library_view,home_view,login_view,logout_view,activation_view
from Register.views import regist_view
from Search.views import search_view
from Email.views import email_view
from Update.views import update_view
from Stream.views import stream_view,torrent_view,post_comment
from Profile.views import history,history_view
urlpatterns = [
    path('', login_view, name='login'),
    path('home/',home_view,name='home'),
    path('search/',search_view,name='search'),
    path('logout/',logout_view,name='logout'),
    path('library/',library_view,name='library'),
    path('update/',update_view,name='update'),
    path('email/',email_view,name='email'),
    path('history/',history,name='history'),
    path('history_view/',history_view,name='history_view'),
    path('torrent_view/',torrent_view,name='torrent_view'),
    path('register/',regist_view,name='register'),
    path('post_comment/',post_comment,name='post_comment'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset_new.html"),name="password_reset_confirm"),
    path('reset_password_complete/>',auth_views.PasswordResetCompleteView.as_view(template_name="reset_login.html"),name="password_reset_complete"),
    
    path('admin/', admin.site.urls),
    path('activation/<user1>/<token1>/',activation_view,name='activation'),
    path('stream/',stream_view),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
# class Playlist(models.Model):
    # STATUS    = (
                # ("Public","Public"),
                # ("Private","Private"),
            # )
    # playlist_name = models.TextField(blank=False,max_length=240)
    # playlist_owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    # playlist_members = models.TextField(blank=False,max_length=1000)
    # playlist_id = models.TextField(blank=False,max_length=20)
    # playlist_status =models.CharField(max_length=7,choices=STATUS,default="Public")
    # def __str__(self):
        # return '%s [%s](%s)' % (self.playlist_name, self.playlist_status,self.playlist_owner)

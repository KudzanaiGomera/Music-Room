from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.utils.text import slugify
from django.utils import timezone

MUSIC_PREFERENCES = (
    ('pop', 'POP'),
    ('country', 'COUNTRY'),
    ('rnb', 'RNB'),
)

# Create your models here.

class Profile(models.Model):
   user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
   music_preferences = models.CharField(choices=MUSIC_PREFERENCES, max_length=100, null=True)
   date_created = models.DateTimeField(auto_now_add=True, null=True)

   def __str__(self):
      return f'{self.user.username} Profile'

   def save(self, *args, **kwargs):
      super(Profile, self).save(*args, **kwargs)


class Playlist(models.Model):
    STATUS    = (
                ("Public","Public"),
                ("Private","Private"),
            )
    playlist_name = models.TextField(blank=False,max_length=240)
    playlist_owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    owner_access_token = models.TextField(blank=False,max_length=20)
    playlist_members = models.TextField(blank=False,max_length=1000)
    playlist_id = models.TextField(blank=False,max_length=20)
    playlist_status =models.CharField(max_length=7,choices=STATUS,default="Public")
    def __str__(self):
        return '%s [%s](%s)' % (self.playlist_name, self.playlist_status,self.playlist_owner)



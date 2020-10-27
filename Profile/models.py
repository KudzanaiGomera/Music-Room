from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class User_Profile(models.Model):
    LANGUAGE    = (
                ("ENG","English"),
                ("GER","German"),
                ("FRE","French"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language        = models.CharField(max_length=20,choices=LANGUAGE,default="ENG")
    picture = models.ImageField(default='default_user.png')
    def __str__(self):
            return f'{self.user}'

def create_profile(sender,instance,created, **kwargs):
    if created:
       User_Profile.objects.create(user=instance)
       
post_save.connect(create_profile,sender=User)

def update_profile(sender,instance,created, **kwargs):
    if created == False:
        instance.user_profile.save()

class Playlist(models.Model):
    STATUS    = (
                ("Public","Public"),
                ("Private","Private"),
            )
    playlist_name = models.TextField(blank=False,max_length=240)
    playlist_owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    playlist_members = models.TextField(blank=False,max_length=1000)
    playlist_id = models.TextField(blank=False,max_length=20)
    playlist_status =models.CharField(max_length=7,choices=STATUS,default="Public")
    def __str__(self):
        return '%s [%s](%s)' % (self.playlist_name, self.playlist_status,self.playlist_owner)

# 
#Create your models here.
# 
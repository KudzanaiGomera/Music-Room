from django.db import models
from django.utils import timezone

# Create your models here.
class Song(models.Model):
    track_id = models.IntegerField(null=False)
    artist_name = models.CharField(max_length=100)
    song_title = models.TextField(max_length=1000)
    track_preview = models.URLField()
    artist_image = models.URLField()
    convert_time = models.CharField(max_length=100)

    # def save(self, *args, **kwargs):
    #     super(Song, self).save(*args, **kwargs)

    def __str__(self):
        return self.song_title
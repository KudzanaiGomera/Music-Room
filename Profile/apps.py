from django.apps import AppConfig
from django.db.models.signals import post_save

class ProfileConfig(AppConfig):
    name = 'Profile'

def ready(self):
    import Profile.signals

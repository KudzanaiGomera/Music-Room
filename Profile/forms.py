from django import forms
class CommentForm(forms.Form):
       user = forms.CharField()
       body = forms.CharField()
class HistoryForm(forms.Form):
       user = forms.CharField()
       title = forms.CharField()
       poster = forms.CharField()
       imdb = forms.CharField()
class PlaylistForm(forms.Form):
       playlist_name= forms.CharField()
       
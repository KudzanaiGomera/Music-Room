from django import forms

# class UpdateForm(forms.Form):
#     picture = forms.ImageField(default='/static/images/default_user.png')
#     ENGLISH     = 'ENG'
#     GERMAN      = 'DEK'
#     FRENCH      = 'FRE'
#     LANGUAGE    = [
       #     (ENGLISH,'English'),
       #     (GERMAN,'German'),
       #     (FRENCH,'French'),
       #     ]
#     language  = forms.CharField(widget=forms.Select(choices=LANGUAGE))

class LoginForm(forms.Form):
       username = forms.CharField()
       password = forms.CharField(widget=forms.PasswordInput())






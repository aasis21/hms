from django import forms

from .models import Post

class PostCreateForm(forms.Form):
    post_name = forms.CharField(label = 'Post Name', max_length=200)
    post = forms.CharField(label = 'Post Username', max_length = 50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class PostHolderForm(forms.Form):
    post = forms.CharField(label = 'Post Username', max_length=200)
    user = forms.CharField(label = 'User Username', max_length = 50)

class RoomChangeForm(forms.Form):
    user = forms.CharField(label = 'Username', max_length=20)
    room = forms.CharField(label = 'Room Number', max_length = 10)

from django import forms

from .models import Post

class PostCreateForm(forms.Form):
    post_name = forms.CharField(label = 'Post Name', max_length=200)
    post = forms.CharField(label = 'Post Username', max_length = 50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class AnnouncementForm(forms.Form):
    heading=forms.CharField(label = 'Heading', max_length=200)
    content=forms.CharField(widget=forms.Textarea)
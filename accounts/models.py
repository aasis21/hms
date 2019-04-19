from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from diafo.models import Questionnaire

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default='')
    roll_no=models.IntegerField(default=0)
    branch=models.CharField(max_length=40,default='')
    program=models.CharField(max_length=10,default='')
    room=models.CharField(max_length=10,default='')
    address = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=255, default='')
    post_holders = models.ManyToManyField(User, blank = True, related_name='posts')

    def __str__(self):
        return self.user.username

class PostHistory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null = True, blank = True)
    def __str__(self):
        return self.user.username + "_" + self.post.user.username

class Announcement(models.Model):
    user = models.ForeignKey(Post, on_delete=models.CASCADE)
    heading=models.CharField(max_length=200)
    content=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

class Form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.OneToOneField(Questionnaire,on_delete=models.CASCADE)



def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
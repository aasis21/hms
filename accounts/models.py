from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, default='None')
    last_name = models.CharField(max_length=255, default='None')
    roll_no=models.IntegerField(default=0)
    branch=models.CharField(max_length=40,default='None')
    program=models.CharField(max_length=10,default='None')
    block=models.CharField(max_length=1,default='None')
    room_no=models.IntegerField(default=0)
    city = models.CharField(max_length=255, default='None')
    state = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.user.username
    @property
    def name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
    @property
    def room(self):
        return '{0} {1}'.format(self.block, self.room_no)
    @property
    def address(self):
        return '{0}, {1}'.format(self.city, self.state)

class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=255, default='')
    post_holders = models.ManyToManyField(User, related_name='posts')

def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
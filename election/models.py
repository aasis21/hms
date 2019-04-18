from django.db import models
from django.contrib.auth.models import User

from diafo.models import Questionnaire, FilledForm

class Survey(models.Model):
    title = models.CharField(max_length=200)
    questionnaire = models.OneToOneField(Questionnaire, null=True ,on_delete=models.CASCADE)

PHASE_CHOICES = (
    ('IP', 'Initial Phase'),
    ('NP', 'Nomination Phase'),
    ('CP', 'Campaign Phase'),
    ('PP', 'Polling Phase'),
    ('OPP', 'Offline Polling Phase'),
    ('MP', 'Mid Phase'),
    ('RP', 'Result Phase'),  
    ('EP', 'End Phase')

)
class Entity(models.Model):
    title = models.CharField(max_length = 500)
    description = models.TextField(max_length=2000)
    nomination = models.OneToOneField(Questionnaire, null=True, on_delete=models.CASCADE)
    phase = models.CharField(max_length=30, choices=PHASE_CHOICES, default = 'IP')
    batch = models.CharField(max_length = 100, default = "all")

    def __str__(self):
        return self.title

class EntityCandidate(models.Model):
    entity = models.ForeignKey(Entity,related_name='candidates', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete =  models.CASCADE )
    response = models.ForeignKey(FilledForm,on_delete=models.CASCADE)
    readme = models.TextField(max_length=5000)
    approval = models.BooleanField(default=True)
    phase = models.CharField(max_length = 30, default= "IP")
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class EntityVotecast(models.Model):
    entity = models.ForeignKey(Entity,related_name='votes', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete =  models.CASCADE )

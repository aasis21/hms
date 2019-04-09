from django.db import models
from django.contrib.auth.models import User

from diafo.models import Questionnaire

class Survey(models.Model):
    title = models.CharField(max_length=200)
    questionnaire = models.OneToOneField(Questionnaire, null=True ,on_delete=models.CASCADE)

PHASE_CHOICES = (
    ('NP', 'Nomination Phase'),
    ('CP', 'Campaign Phase'),
    ('PP', 'Polling Phase'),
    ('RP', 'Result Phase'),
    ('BP', 'Blank Phase')
)
class Entity(models.Model):
    title = models.CharField(max_length = 500)
    description = models.TextField(max_length=2000)
    nomination = models.OneToOneField(Questionnaire, null=True, on_delete=models.CASCADE)
    phase = models.CharField(max_length=30, choices=PHASE_CHOICES, default = 'BP')

class EntityCandidate(models.Model):
    enity = models.ForeignKey(Entity, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete =  models.CASCADE )
    readme = models.TextField(max_length=5000)
    approval = models.BooleanField(default=True)
    phase = models.CharField(max_length = 30)
    votes = models.IntegerField(default=0)


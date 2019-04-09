from django.db import models

from diafo.models import Questionnaire

class Survey(models.Model):
    title = models.CharField(max_length=200)
    questionnaire = models.OneToOneField(Questionnaire, null=True,on_delete=models.CASCADE)
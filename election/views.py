from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from . import models
from diafo.models import Questionnaire

@login_required
def create_entity(request):
#     if request.user.username = "ec":
        
#     else:
#         return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

    questionnaire = Questionnaire.objects.create(name="sdghs")
    survey = models.Survey.objects.create(title="djhfkjhdj", questionnaire = questionnaire)
    return HttpResponseRedirect(reverse('diafo:admin_view', kwargs={'pk': survey.questionnaire.pk}))

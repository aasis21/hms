from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from . import models
from diafo.models import Questionnaire
from . import forms

@login_required
def create_entit(request):
#     if request.user.username = "ec":
        
#     else:
#         return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

    questionnaire = Questionnaire.objects.create(name="sdghs")
    survey = models.Survey.objects.create(title="djhfkjhdj", questionnaire = questionnaire)
    return HttpResponseRedirect(reverse('diafo:admin_view', kwargs={'pk': survey.questionnaire.pk}))

def create_entity(request):
    if request.user.username == "ec":
        form = forms.EntityCreateForm()
        if request.method == "POST":
            form = forms.EntityCreateForm(request.POST)
            if form.is_valid():
                form_title = form.cleaned_data["form_title"]
                entity_title = form.cleaned_data["entity_title"]
                desc = form.cleaned_data["description"]
                questionnaire = Questionnaire.objects.create(name= form_title)
                models.Entity.objects.create(title = form.cleaned_data, description = desc, nomination = questionnaire)
                return render(request, 'message.html', { 'message' : 'New entity made' , 'code' : '404' })
        
        return render(request, 'election/entity_create.html', {'form': form})

    else:
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })


@login_required
def index(request):
    result_phase = models.Entity.objects.filter(phase = "RP")
    poll_phase = models.Entity.objects.filter(phase = "PP")
    nomination_phase = models.Entity.objects.filter(phase = "NP")
    campaign_phase = models.Entity.objects.filter(phase = "CP")

    t_data= {'result' : result_phase, 
            'poll': poll_phase, 
            'nomination' : nomination_phase,
            'campaign': campaign_phase,
    }

    if request.user.username == "ec":
        blank_phase = models.Entity.objects.filter(phase="BP")
        return render(request, 'election/index.html', {**t_data, 'blank' :  blank_phase, 'ec': True})
    else:
        return render(request, 'election/index.html', { **t_data, 'ec' : False})

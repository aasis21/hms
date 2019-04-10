from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
from . import models
from diafo.models import Questionnaire, FilledForm
from . import forms

@login_required
def create_form(request):
#     if request.user.username = "ec":
        
#     else:
#         return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

    questionnaire = Questionnaire.objects.create(name="Hall President Nomination")
    survey = models.Survey.objects.create(title="djhfkjhdj", questionnaire = questionnaire)
    return HttpResponseRedirect(reverse('diafo:admin_view', kwargs={'pk': survey.questionnaire.pk}))

@login_required 
def offline_polling(request):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })
    offline_phase = models.Entity.objects.filter(phase="OPP")
    return render(request, 'election/offline_polling.html', {'offline': offline_phase})

    
@login_required
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
                entity = models.Entity.objects.create(title = entity_title, description = desc, nomination = questionnaire)
                
                nota = User.objects.get(username='nota')
                response = questionnaire.add_answer(nota, '')
                models.EntityCandidate.objects.create(entity = entity, user = nota, readme = "I am NOTA" , response = response)

                return HttpResponseRedirect(reverse('election:entity_detail_ec', kwargs={'pk': entity.pk}))
        
        return render(request, 'election/entity_create.html', {'form': form})
    else:
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

@login_required
def entity_detail_user(request, pk):
    try:
        entity = models.Entity.objects.get(pk=pk)
    except:
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })
    
    candidates = entity.candidates.filter(approval=True)
    phase = entity.phase
    if phase == "BP":
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

    phase_dict = {'IP':'Initial Phase', 'NP': 'Nomination Phase','CP' : 'Campaign Phase', 'PP': 'Polling Phase', 'OPP': 'Offline Polling Phase','MP': 'Mid Phase', 'RP': 'Result Phase', 'EP': 'End Phase' }
    
    manifesto_form = forms.NomiManifestoForm()
    
    nota = User.objects.get(username = "nota")
    cast_form = forms.PollForm(initial={ 'candidates' : models.EntityCandidate.objects.filter(entity = entity, user=nota).first() })
    cast_form.fields['candidates'].queryset = models.EntityCandidate.objects.filter(entity = entity, approval = True)

    return render(request, 'election/entity_detail_user.html',{'entity': entity, 'candidates': candidates, 'phase' : phase_dict[phase], \
            'manifesto_form' : manifesto_form, 'result' : candidates.order_by('-votes'), 'cast_form' : cast_form })

def entity_offline_poll(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })
    try:
        entity = models.Entity.objects.get(pk=pk)
    except:
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })
    
    phase = entity.phase
    if phase != "OPP":
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

    candidates = entity.candidates.filter(approval=True)
    nota = User.objects.get(username = "nota")
    cast_form = forms.PollForm(initial={ 'candidates' : candidates.filter(user=nota).first() })
    cast_form.fields['candidates'].queryset = candidates


    return render(request, 'election/entity_offline_poll.html',{'entity': entity, 'candidates': candidates, 'cast_form': cast_form})


@login_required
def entity_detail_ec(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })

    try:
        entity = models.Entity.objects.get(pk=pk)
    except:
        return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })
    
    phase = entity.phase
    candidates = entity.candidates.all()
    phase_dict = {'IP':'Initial Phase', 'NP': 'Nomination Phase','CP' : 'Campaign Phase', 'PP': 'Polling Phase', 'OPP': 'Offline Polling Phase','MP': 'Mid Phase', 'RP': 'Result Phase', 'EP': 'End Phase' }

    phase_change_form = forms.PhaseChangeForm(initial={'phase': phase})
    edit_desciption_form = forms.EditDescriptionForm(initial={'description' : entity.description})


    return render(request, 'election/entity_detail_ec.html',{'entity': entity, 'candidates': candidates, 'phase' : phase_dict[phase], \
        'phase_change_form': phase_change_form, 'edit_description_form' : edit_desciption_form })


@login_required
@require_http_methods(["GET"])
def approval_accept(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })
    entity = models.EntityCandidate.objects.get(pk=pk)
    entity.approval = True
    entity.phase = entity.entity.phase
    entity.save()
    return HttpResponseRedirect(reverse('election:entity_detail_ec', kwargs={'pk': entity.entity.pk}))
    
@login_required
@require_http_methods(["GET"])
def approval_reject(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })
    entity = models.EntityCandidate.objects.get(pk=pk)
    entity.approval = False
    entity.phase = entity.entity.phase
    entity.save()
    return HttpResponseRedirect(reverse('election:entity_detail_ec', kwargs={'pk': entity.entity.pk}))

@login_required
@require_http_methods(["POST"])
def phase_edit(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })
    entity = models.Entity.objects.get(pk=pk)
    phase_change_form = forms.PhaseChangeForm(request.POST)
    if phase_change_form.is_valid():
        entity.phase = phase_change_form.cleaned_data['phase']
        entity.save()
        return HttpResponseRedirect(reverse('election:entity_detail_ec', kwargs={'pk': pk}))
    else:
        return render(request, 'message.html', { 'message' : 'Form input Not valid' , 'code' : '404' })

@login_required
@require_http_methods(["POST"])
def description_edit(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })
    entity = models.Entity.objects.get(pk=pk)
    edit_desciption_form = forms.EditDescriptionForm(request.POST)
    if edit_desciption_form.is_valid():
        entity.description = edit_desciption_form.cleaned_data['description']
        entity.save()
        return HttpResponseRedirect(reverse('election:entity_detail_ec', kwargs={'pk': pk}))
    else:
        return render(request, 'message.html', { 'message' : 'Form input Not valid' , 'code' : '404' })

@login_required
@require_http_methods(["POST"])
def cast_vote(request, pk):
    entity = models.Entity.objects.get(pk=pk)
    phase = entity.phase
    if phase != "PP":
        return render(request, 'message.html', { 'message' : 'Not in Polling phase' , 'code' : '404' })

    cast_form = forms.PollForm(request.POST)
    if cast_form.is_valid():
        vote_candidate =  cast_form.cleaned_data['candidates']
        vote_candidate = User.objects.get(username = vote_candidate)

        check_for_vote = entity.votes.filter(user = request.user)
        if check_for_vote.exists():
            return render(request, 'message.html', { 'message' : 'Can not vote Twice' , 'code' : '404' })
        entity_candidate = entity.candidates.filter(user = vote_candidate).first()
        entity_candidate.votes = entity_candidate.votes  + 1
        entity_candidate.save()
        models.EntityVotecast.objects.create(entity = entity, user = request.user)
        return render(request, 'message.html', { 'message' : 'Vote Casted Successfully' , 'code' : '200' })

    else:
        return render(request, 'message.html', { 'message' : 'Form input Not valid' , 'code' : '404' })

@login_required
@require_http_methods(["POST"])
def cast_vote_offline(request, pk):
    if request.user.username != "ec":
        return render(request, 'message.html', { 'message' : 'Page Not Found'  , 'code' : '404' })

    entity = models.Entity.objects.get(pk=pk)
    phase = entity.phase
    if phase != "OPP":
        return render(request, 'message.html', { 'message' : 'Not in Polling phase' , 'code' : '404' })
    cast_form = forms.PollForm(request.POST)
    if cast_form.is_valid():
        vote_candidate =  cast_form.cleaned_data['candidates']
        vote_candidate = User.objects.get(username = vote_candidate)
        entity_candidate = entity.candidates.filter(user = vote_candidate).first()
        entity_candidate.votes = entity_candidate.votes  + 1
        entity_candidate.save()
        return render(request, 'message.html', { 'message' : 'Vote Casted Successfully' , 'code' : '200' })

    else:
        return render(request, 'message.html', { 'message' : 'Form input Not valid' , 'code' : '404' })

    
@login_required
@require_http_methods(["POST"])
def file_nomination(request, pk):
    try:
        entity = models.Entity.objects.get(pk=pk)
        phase = entity.phase
        if phase != "NP":
            return render(request, 'message.html', { 'message' : 'Page Not Found' , 'code' : '404' })

        manifesto_form = forms.NomiManifestoForm(request.POST)
        if manifesto_form.is_valid():
            manifesto =  manifesto_form.cleaned_data['manifesto']
            check_for_filled = entity.candidates.filter(user = request.user)
            if check_for_filled.exists():
                return render(request, 'message.html', { 'message' : 'Can not file Nomination Twice' , 'code' : '404' })
            
            nomination_response = entity.nomination.filledform_set.filter(applicant = request.user)

            if not nomination_response.exists():
                return render(request, 'message.html', { 'message' : 'First fill the Nomination Form' , 'code' : '404' })

            response = nomination_response.last()

            models.EntityCandidate.objects.create(entity = entity, user = request.user,response = response, readme = manifesto)
            return render(request, 'message.html', { 'message' : 'Nomination Filed Successfully' , 'code' : '200' })
        else:
            return render(request, 'message.html', { 'message' : 'Form input Not valid' , 'code' : '404' })
    except:
        return render(request, 'message.html', { 'message' : 'Page Not Found s'  , 'code' : '404' })



@login_required
def index(request):
    nomination_phase = models.Entity.objects.filter(phase = "NP")
    campaign_phase = models.Entity.objects.filter(phase = "CP")
    poll_phase = models.Entity.objects.filter(phase = "PP")
    result_phase = models.Entity.objects.filter(phase = "RP")
    
    t_data= {'result' : result_phase, 
            'poll': poll_phase, 
            'nomination' : nomination_phase,
            'campaign': campaign_phase,
    }

    if request.user.username == "ec":
        initial_phase = models.Entity.objects.filter(phase="IP")
        mid_phase = models.Entity.objects.filter(phase="MP")
        offline_phase = models.Entity.objects.filter(phase="OPP")
        end_phase = models.Entity.objects.filter(phase="EP")
        ec_data= {'initial' : initial_phase, 
                'mid': mid_phase, 
                'offline' : offline_phase,
                'end': end_phase,
        }
        return render(request, 'election/index.html', {**t_data, **ec_data , 'ec': True})
    else:
        return render(request, 'election/index.html', { **t_data, 'ec' : False})

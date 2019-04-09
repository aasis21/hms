from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Questionnaire, Question , FilledForm
from .forms import  AddQuestionForm , EditQuestionForm, EditDetailForm
import json



def user_view(request,view_id):
    questionnaire = Questionnaire.objects.get(view_id = view_id)
    form = questionnaire.get_form(request.POST or None)
    if form.is_valid():
        if questionnaire.requires_sign_in and questionnaire.collect_identity:
            if request.user:
                 filled_form = questionnaire.add_answer(request.user, form.cleaned_data)
            else:
                filled_form = questionnaire.add_answer(None,form.cleaned_data)
        else:
            filled_form = questionnaire.add_answer(None, form.cleaned_data)

        return render(request, 'diafo/info.html', context={'info':'Response Recorded'})

    if questionnaire.requires_sign_in:
        if request.user.is_authenticated:
            return render(request, 'diafo/user_view.html', context={'form': form,'title': questionnaire.name,
                                                                    'view_id': questionnaire.view_id})
        else:
            return render(request,'diafo/info.html',context={'info':'Sign_in required'})
    else:
        return render(request, 'diafo/user_view.html',
                      context={'form': form, 'title': questionnaire.name, 'view_id': questionnaire.view_id})


@login_required
def view_filled_form(request,pk):
    filled_form = FilledForm.objects.get(pk =pk)
    data = json.loads(filled_form.data)
    questionnaire = filled_form.questionnaire
    title =  questionnaire.name
    form = questionnaire.get_form(data)
    if filled_form.applicant:
        applicant = filled_form.applicant
    else:
        applicant = 'none'
    return render(request, 'diafo/view_filled_form.html', context={'form': form,'title':title,'applicant':applicant})

@login_required
def admin_view(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    form = questionnaire.get_form(request.POST or None)
    pk = questionnaire.pk
    view_id = questionnaire.view_id
    questions = Question.objects.filter(questionnaire=questionnaire)
    responses = questionnaire.filledform_set.all()
    count = questionnaire.filledform_set.count()

    detail_form = EditDetailForm(request.POST or None, instance=questionnaire)
    if detail_form.is_valid():
        detail_form.save()
        return HttpResponseRedirect(reverse('diafo:admin_view', kwargs={'pk': pk}))



    return render(request, 'diafo/admin_view.html',
                  context={'form': form,'detail_form': detail_form ,'questions': questions,'count': count,
                           'title': questionnaire.name,'pk':questionnaire.pk,'view_id':view_id,'responses':responses})



@login_required
def add_question(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            Question.objects.create(questionnaire=questionnaire, question_type=form.cleaned_data['question_type'],
                                    question=form.cleaned_data['question'],
                                    question_choices=form.cleaned_data['question_choices'],
                                    required=form.cleaned_data['required'])

            return HttpResponseRedirect(reverse('diafo:admin_view', kwargs={'pk': questionnaire.pk}))
    else:
        form = AddQuestionForm()

        return render(request, 'diafo/add_ques.html', context={'form': form})




@login_required
def edit_question(request, pk,ques_id):
    try:
        question = Question.objects.get(pk = ques_id)
        questionnaire = Questionnaire.objects.get(pk = pk)
    except:
        return render(request,'diafo/info.html')
    if question.questionnaire == questionnaire:
        form = EditQuestionForm(request.POST or None, instance=question)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('diafo:admin_view', kwargs={'pk':pk}))

        return render(request, 'diafo/edit_ques.html', context={'form': form})

    else:
        return render(request, 'diafo/info.html',context={'info':'No Access'})

@login_required
def delete_question(request,pk,ques_id):
    try:
        question = Question.objects.get(pk = ques_id)
        questionnaire = Questionnaire.objects.get(pk = pk)
    except:
        return render(request,'diafo/info.html')

    if question.questionnaire == questionnaire:
        question.delete()
    else:
        return render(request,'diafo/info.html', context={'info':'No Access'})



@login_required
def replicate(pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    new_questionnaire = Questionnaire.objects.create()
    for question in questionnaire.question_set.all():
        Question.objects.create(questionnaire=new_questionnaire, question_type=question.question_type,
                                question=question.question,
                                question_choices=question.question_choices)

    return new_questionnaire




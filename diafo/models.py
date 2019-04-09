# Create your models here.
from django.db import models
from django import forms
from django.contrib.auth.models import User
from .form_dynamic import CreatedForm
import json
import uuid
from datetime import datetime,date
from django.utils import timezone

class Questionnaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    view_id = models.CharField(max_length=50,unique=True, default=uuid.uuid4)

    name = models.CharField(max_length=200, null=True)
    requires_sign_in = models.BooleanField(default = False, blank = True)
    collect_identity = models.BooleanField(default = False, blank = True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_form(self, *args, **kwargs):
        fields = []
        for question in self.question_set.all():
            field = question._get_formfield_class()
            label = question.question

            if question.required:
                label = question.question + " *"

            field_args = question._get_field_args()

            ques_id = question.id

            fields.append((label, field, field_args, ques_id))

        return CreatedForm(*args, extra=fields, **kwargs)

    def add_answer(self,applicant, answer_data):
        json_data = json.dumps(answer_data)
        if applicant:
            answerform = FilledForm(questionnaire=self,applicant=applicant,data=json_data)
        else:
            answerform = FilledForm(questionnaire=self,data=json_data)
        answerform.save()
        return answerform


FIELD_TYPES = (
    ('Short_answer', forms.CharField),
    ('Paragraph', forms.CharField),
    ('Integer', forms.IntegerField),
    ('ChoiceField', forms.ChoiceField),
    ('MultipleChoiceField', forms.MultipleChoiceField),
    # ('Date', diafo.DateField),
)

QUES_TYPES = (
    ('Short_answer', 'One Line Answer'),
    ('Paragraph', 'Multiple Line Answer'),
    ('Integer', 'Integer Answer'),
    ('ChoiceField', 'Choice'),
    ('MultipleChoiceField', 'Multiple-choice'),
    # ('Date', 'date'),
)


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire,on_delete=models.CASCADE, null=True)
    question_type = models.CharField(max_length=50, choices=QUES_TYPES, null=True)
    question = models.CharField(max_length=1000, null=True)
    question_choices = models.TextField(max_length=600, null=True, blank=True, help_text='make new line for new option')
    required = models.BooleanField(default=True)

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.question

    def _get_formfield_class(self):
        for index, field_class in FIELD_TYPES:
            if self.question_type == index:
                return field_class

    def _get_field_args(self):
        args = {}
        if self.question_type == 'ChoiceField' or self.question_type == 'MultipleChoiceField':
            args['choices'] = enumerate(self.question_choices.split('\n'))

        if self.question_type == 'MultipleChoiceField':
            args['widget']=forms.CheckboxSelectMultiple

        if self.question_type == 'Paragraph':
            args['widget'] =forms.Textarea

        if self.required:
            args['label_suffix'] = " *"

        args.update({'required': self.required})

        return args


class FilledForm(models.Model):
    id = models.CharField(max_length = 50, primary_key=True, default=uuid.uuid4, editable=False,unique = True)
    questionnaire = models.ForeignKey(Questionnaire,on_delete=models.CASCADE, null=True)
    applicant = models.ForeignKey(User,related_name = 'filled_forms', on_delete=models.CASCADE, null=True , blank = True)
    data = models.CharField(max_length=30000, null=True, blank=True)
    timestamp = models.DateField(default=timezone.now)
    edit_time = models.DateField(null=True, default=timezone.now)

    def __str__(self):
        return self.questionnaire.name





from django import forms
from . import models

from bootstrap4.widgets import RadioSelectButtonGroup
import datetime
now = datetime.datetime.now().year

BATCH_CHOICE = [("all", "All")] + [ ( str(i)[2:] , "Y" + str(i)[2:]   ) for i in range(now - 5, now + 2) ] 

class EntityCreateForm(forms.Form):
    entity_title = forms.CharField(label = 'Election Entity Name', max_length=200)
    description = forms.CharField(label = "Description", widget = forms.Textarea, max_length= 2000)
    form_title = forms.CharField(label = 'Nomination Form Title', max_length= 200)
    batch = forms.MultipleChoiceField(label = 'Batch criterion', widget=forms.CheckboxSelectMultiple, choices= BATCH_CHOICE)

class NomiManifestoForm(forms.Form):
    manifesto = forms.CharField(label = "Manifesto", widget = forms.Textarea, max_length= 5000)

class PollForm(forms.Form):
    candidates = forms.ModelChoiceField(queryset=models.EntityCandidate.objects.all(), widget= RadioSelectButtonGroup, empty_label=None , label="" )

class PhaseChangeForm(forms.Form):
    phase = forms.ChoiceField(choices=models.PHASE_CHOICES)

class EditDescriptionForm(forms.Form):
    description = forms.CharField(label = "", widget = forms.Textarea, max_length= 2000)


from django import forms
from . import models

from bootstrap4.widgets import RadioSelectButtonGroup

class EntityCreateForm(forms.Form):
    entity_title = forms.CharField(label = 'Election Entity Name', max_length=200)
    description = forms.CharField(label = "Description", widget = forms.Textarea, max_length= 2000)
    form_title = forms.CharField(label = 'Nomination Form Title', max_length= 200)

class NomiManifestoForm(forms.Form):
    manifesto = forms.CharField(label = "Manifesto", widget = forms.Textarea, max_length= 5000)

class PollForm(forms.Form):
    candidates = forms.ModelChoiceField(queryset=models.EntityCandidate.objects.all(), widget= RadioSelectButtonGroup, empty_label=None , label="" )

class PhaseChangeForm(forms.Form):
    phase = forms.ChoiceField(choices=models.PHASE_CHOICES)

class EditDescriptionForm(forms.Form):
    description = forms.CharField(label = "", widget = forms.Textarea, max_length= 2000)


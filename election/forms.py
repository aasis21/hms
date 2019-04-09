from django import forms

class EntityCreateForm(forms.Form):
    entity_title = forms.CharField(label = 'Election Entity Name', max_length=200)
    description = forms.CharField(label = "Description", widget = forms.Textarea, max_length= 2000)
    form_title = forms.CharField(label = 'Nomination Form Title', max_length= 200)

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class BillForm(forms.Form):
    user = forms.CharField(max_length=100,required=True)
    reason = forms.CharField(max_length=150,required=False)
    bill = forms.IntegerField(required=True)

class MessForm(forms.Form):
    start_data=forms.DateField(widget = forms.SelectDateWidget(),required=True)
    end_data=forms.DateField(widget = forms.SelectDateWidget(),required=True)
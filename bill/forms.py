from django import forms

class BillForm(forms.Form):
    user = forms.CharField(max_length=100,required=True)
    reason = forms.CharField(max_length=150,required=False)
    bill = forms.IntegerField(required=True)

from django import forms
from .models import QUES_TYPES,Question, Questionnaire



class AddQuestionForm(forms.Form):

    question_type = forms.CharField(max_length=50,widget=forms.Select(choices=QUES_TYPES))
    question = forms.CharField(max_length=400)
    question_choices = forms.CharField(max_length=512,widget=forms.Textarea,label_suffix=' *',
                                       help_text='add choices in separate lines', required=False)
    required = forms.BooleanField(initial=True,required = False)


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_type','question','question_choices','required')


class EditDetailForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        labels = {
            "name": "Title"}
        fields = ('name','requires_sign_in','collect_identity')
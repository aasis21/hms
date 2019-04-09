from django.contrib import admin
from .models import Questionnaire, FilledForm


# Register your models here.

admin.site.register(Questionnaire)
admin.site.register(FilledForm)

from django.urls import path, re_path

from . import views

app_name = 'election'

urlpatterns = [
    path('create_entity/', views.create_entity, name='create_entity'),
]
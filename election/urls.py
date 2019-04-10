from django.urls import path, re_path

from . import views

app_name = 'election'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_entity/', views.create_entity, name='create_entity'),
    path('create_form/', views.create_form, name='create_form'),
    path('entity/<int:pk>/', views.entity_detail_user, name='entity_detail_user'),
    path('entity_ec/<int:pk>/', views.entity_detail_ec, name='entity_detail_ec'),
    path('file_nomination/<int:pk>/', views.file_nomination, name='file_nomination'),
    path('cast_vote/<int:pk>/', views.cast_vote, name='cast_vote'),
    path('reject/<int:pk>', views.approval_reject, name='approval_reject'),
    path('accept/<int:pk>', views.approval_accept, name='approval_accept'),
    path('phase_edit/<int:pk>', views.phase_edit, name='phase_edit'),
    path('description_edit/<int:pk>', views.description_edit, name='description_edit'),

]
from django.urls import path, re_path

from . import views

app_name = 'bills'

urlpatterns = [
    path('', views.bill, name='bill'),
    path('addbill', views.addbill, name='addbill'),
    path('transiction', views.transiction, name='transiction'),
]
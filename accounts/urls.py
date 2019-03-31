from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('profile/', views.profile, name='profile'),
]
from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('logout/', views.sign_out, name='sign_out'),
    path('profile/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
]
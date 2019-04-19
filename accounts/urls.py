from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/login/', views.sign_in, name='sign_in'),
    path('accounts/sign_up/', views.sign_up, name='sign_up'),
    re_path(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('accounts/logout/', views.sign_out, name='sign_out'),
    path('profile/', views.profile, name='profile'),
    path('', views.dashboard, name='entry'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('announcement/', views.add_announcement, name='announcement'),
    path('add_postholder/', views.add_post_holder, name='postholder_add'),
    path('posts/', views.posts, name='posts'),
    path('post/<str:post_id>', views.post_detail, name='post_detail'),
    path('user_profile/<str:user_id>', views.user_profile, name='user_profile'),
    path('create_form', views.create_form, name='create_form'),
    path('forms', views.user_forms, name='user_forms'),
    path('change_room', views.change_room, name = 'change_room')

]

from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('logout/', views.sign_out, name='sign_out'),
    path('profile/', views.dashboard, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('announcement/', views.add_announcement, name='announcement'),
    path('add_postholder/', views.add_post_holder, name='postholder_add'),
    path('posts/', views.posts, name='posts'),
    path('post/<str:post_id>', views.post_detail, name='post_detail'),
    path('user_profile/<str:user_id>', views.profile, name='user_profile')
]

from . import views
from django.urls import path, re_path

app_name = 'diafo'

urlpatterns = [

    re_path(r'^admin/(?P<pk>[0-9a-f-]+)/$', views.admin_view, name='admin_view'),
    re_path(r'^admin/add_ques/(?P<pk>[0-9a-f-]+)/$', views.add_question, name='add_question'),
    re_path(r'^admin/edit_ques/(?P<pk>[0-9a-f-]+)/(?P<ques_id>\d+)/$',views.edit_question,name='edit_question'),
    re_path(r'^user/view/(?P<view_id>[0-9a-f-]+)/$',views.user_view, name = 'user_view'),
    re_path(r'^view/response/(?P<pk>[0-9a-f-]+)/$', views.view_filled_form, name='view_filled_form'),

]

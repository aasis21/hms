from django.urls import path, re_path

from . import views

app_name = 'grb'

urlpatterns = [
    # path('', views.temp, name='temp'),
    path('', views.select_range, name = 'select_range'),
    path('show/<start_date>/<end_date>', views.show_vacancies, name = 'show_vacancies'),
    path('book/<book_date>', views.book_room, name = 'book_room'),
    path('booking-requests', views.see_requests, name = 'see_requests'),
    path('individual-requests/<username>', views.user_requests, name = 'user_requests'),
    path('delete-request/<pk>', views.delete_requests, name = 'delete_requests'),
    path('approve-request/<pk>', views.approve_requests, name = 'approve_requests'),
    path('approve-all/<username>', views.approve_all, name = 'approve_all'),
    path('delete-all/<username>', views.delete_all, name = 'delete_all')

]

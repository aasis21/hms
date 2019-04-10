import django_tables2 as tables
from .models import Profile
import django_filters
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class SearchFilter(django_filters.FilterSet):
    address=django_filters.CharFilter(field_name='address',lookup_expr='icontains',label='Address')
    name=django_filters.CharFilter(field_name='name',lookup_expr='icontains',label='Name')
    branch=django_filters.CharFilter(field_name='branch',lookup_expr='icontains',label='Branch')
    room=django_filters.CharFilter(field_name='room',lookup_expr='icontains',label='Room')
    user=django_filters.CharFilter(field_name='user__username',lookup_expr='icontains',label='User')

    class Meta:
        model = Profile
        exclude=['email_confirmed']

class SearchTable(tables.Table):
    class Meta:
        model = Profile
        fields=['user','roll_no','name','room','program','branch','address']
        template_name = 'django_tables2/bootstrap.html'

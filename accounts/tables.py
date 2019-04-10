import django_tables2 as tables
from .models import Profile
import django_filters
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class SearchFilter(django_filters.FilterSet):
    state=django_filters.CharFilter(field_name='state',lookup_expr='icontains')
    first_name=django_filters.CharFilter(field_name='first_name',lookup_expr='icontains')
    last_name=django_filters.CharFilter(field_name='last_name',lookup_expr='icontains')
    city=django_filters.CharFilter(field_name='city',lookup_expr='icontains')
    branch=django_filters.CharFilter(field_name='branch',lookup_expr='icontains')
    class Meta:
        model = Profile
        exclude=['email_confirmed']

class SearchTable(tables.Table):
    class Meta:
        model = Profile
        fields=['user','roll_no','name','room','program','branch','address']
        template_name = 'django_tables2/bootstrap.html'

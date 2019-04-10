import django_tables2 as tables
from .models import *
import django_filters
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class TransictionFilter1(django_filters.FilterSet):
    user=django_filters.CharFilter(field_name='user__username',lookup_expr='icontains',label='User')
    class Meta:
        model = Bill
        fields = ['user', 'reason']

class TransictionFilter2(django_filters.FilterSet):
    biller=django_filters.CharFilter(field_name='biller__user__username',lookup_expr='icontains',label='Biller')
    class Meta:
        model = Bill
        fields = ['biller', 'reason']

class MessFilter(django_filters.FilterSet):
    user=django_filters.CharFilter(field_name='user__username',lookup_expr='icontains',label='User')
    class Meta:
        model = Messrem
        exclude=['id']

class BillTable(tables.Table):
    name=tables.Column()
    total_bill=tables.Column()
    class Meta:
        template_name = 'django_tables2/bootstrap.html'

class TransictionTable(tables.Table):
    class Meta:
        model = Bill
        template_name = 'django_tables2/bootstrap.html'

class MessTable(tables.Table):
    Cancel = tables.TemplateColumn(
        template_code='''<a href="{% url 'bills:rmremb' record.id %}">x</a>''',
    )
    class Meta:
        model = Messrem
        fields=['user','start','end']
        template_name = 'django_tables2/bootstrap.html'

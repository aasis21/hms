import django_tables2 as tables
from .models import Bill
import django_filters
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class TransictionFilter1(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = ['user', 'reason']

class TransictionFilter2(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = ['biller', 'reason']

class BillTable(tables.Table):
    name=tables.Column()
    total_bill=tables.Column()
    class Meta:
        template_name = 'django_tables2/bootstrap.html'

class TransictionTable(tables.Table):
    class Meta:
        model = Bill
        template_name = 'django_tables2/bootstrap.html'

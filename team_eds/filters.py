import django_filters
from django_filters import CharFilter

from hr_features.models import *


class OrderFilter(django_filters.FilterSet):
    companyname=CharFilter(field_name='companyname', lookup_expr='icontains')

    class Meta:
        model= Hr
        fields=['companyname','status','interview','transport','branch']
import django_filters
from .models import RepairRequest

class RepairRequestFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    equipment = django_filters.NumberFilter(field_name='equipment__id')

    class Meta:
        model = RepairRequest
        fields = ['status', 'client', 'assigned_to', 'equipment', 'created_after']

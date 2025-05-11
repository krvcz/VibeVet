from django_filters import rest_framework as filters
from .models import UserSearchHistory

class UserSearchHistoryFilter(filters.FilterSet):
    from_date = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    module = filters.CharFilter(field_name='module')

    class Meta:
        model = UserSearchHistory
        fields = ['module', 'from_date', 'to_date']
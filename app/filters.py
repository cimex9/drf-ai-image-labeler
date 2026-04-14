import django_filters
from django_filters.rest_framework import FilterSet

from app.models import Label


class LabelFilter(FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = Label
        fields = {
            'name': ['exact'],
            'created_at': ['gte', 'lte'],
        }

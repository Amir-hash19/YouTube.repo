from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from channle.models import Channel
from django.db.models import Count



class ChannelFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='incontains')
    owner = filters.CharFilter(field_name='owner__username', lookup_expr='exact')
    date_from = filters.DateTimeFilter(field_name='date_created', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='date_created', lookup_expr='lte')


    class Meta:
        model = Channel
        fields = ['title', 'owner', 'date_from', 'date_to']






class SubChannelFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    owner = filters.NumberFilter(field_name="owner__username")
    date_from = filters.DateTimeFilter(field_name="date_created", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="date_created", lookup_expr="lte")
    min_subscribers = filters.NumberFilter(method='filter_min_subscribers')
    max_subscribers = filters.NumberFilter(method='filter_max_subscribers')
    admin = filters.NumberFilter(field_name='admins__username')
    subscriber = filters.NumberFilter(field_name='subscribers__username')

    class Meta:
        model = Channel
        fields = [
            'title', 'owner', 'date_from', 'date_to',
            'min_subscribers', 'max_subscribers',
            'admin', 'subscriber',
        ]

    def filter_min_subscribers(self, queryset, name, value):
        return queryset.annotate(sub_count=Count('subscribers')).filter(sub_count__gte=value)

    def filter_max_subscribers(self, queryset, name, value):
        return queryset.annotate(sub_count=Count('subscribers')).filter(sub_count__lte=value)




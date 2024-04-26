import django_filters

from .models import Providerprofile

class ProvidersFilter(django_filters.FilterSet):
    keyword = django_filters.filters.CharFilter(field_name="username",lookup_expr="icontains")
    minRate = django_filters.filters.NumberFilter(field_name="ratings" or 0,lookup_expr="gte")
    place= django_filters.filters.CharFilter(field_name="city",lookup_expr="iexact")

    class Meta:
        model = Providerprofile
        fields = ('minRate', 'place','keyword')
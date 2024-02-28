import django_filters

from .models import Providerprofile

class ProvidersFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name="username",lookup_expr="icontains")
    minRate = django_filters.filters.NumberFilter(field_name="ratings" or 0,lookup_expr="gte")
    place= django_filters.filters.CharFilter(field_name="city",lookup_expr="iexact")
    # maxPrice = django_filters.filters.NumberFilter(field_name="price" or 100000,lookup_expr="lte")

    class Meta:
        model = Providerprofile
      #  fields = ['category', 'brand']
        fields = ('minRate', 'place','keyword')
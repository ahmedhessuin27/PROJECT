import django_filters
from .models import Userprofile,Providerprofile
class ChatFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(field_name='username',lookup_expr="icontains")

    class Meta:
        model = Userprofile
        fields=('name',)
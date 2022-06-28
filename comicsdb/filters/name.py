from django_filters import rest_framework as filters


class NameFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

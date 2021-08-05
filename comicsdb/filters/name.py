import django_filters


class NameFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

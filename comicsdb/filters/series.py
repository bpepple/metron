import django_filters

from comicsdb.models import Series


class SeriesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    publisher_id = django_filters.filters.NumberFilter(
        field_name="publisher__id", lookup_expr="exact"
    )
    publisher_name = django_filters.CharFilter(
        field_name="publisher__name", lookup_expr="icontains"
    )

    class Meta:
        model = Series
        fields = ["volume", "year_began", "year_end"]

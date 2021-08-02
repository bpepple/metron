import django_filters
from comicsdb.models import Issue


class IssueFilter(django_filters.FilterSet):
    cover_year = django_filters.NumberFilter(
        field_name="cover_date", lookup_expr="year"
    )
    cover_month = django_filters.NumberFilter(
        field_name="cover_date", lookup_expr="month"
    )
    publisher = django_filters.filters.CharFilter(
        field_name="series__publisher__name", lookup_expr="icontains"
    )
    series_name = django_filters.CharFilter(
        field_name="series__name", lookup_expr="icontains"
    )
    series_volume = django_filters.NumberFilter(
        field_name="series__volume", lookup_expr="exact"
    )
    store_date_range = django_filters.filters.DateFromToRangeFilter("store_date")
    series_year_began = django_filters.filters.NumberFilter(
        field_name="series__year_began", lookup_expr="exact"
    )

    class Meta:
        model = Issue
        fields = ["number", "store_date"]

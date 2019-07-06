import django_filters

from comicsdb.models import Issue


class IssueFilter(django_filters.FilterSet):
    series_name = django_filters.CharFilter(
        field_name="series__name", lookup_expr="icontains"
    )
    series_volume = django_filters.NumberFilter(
        field_name="series__volume", lookup_expr="exact"
    )
    cover_year = django_filters.NumberFilter(
        field_name="cover_date", lookup_expr="year"
    )
    cover_month = django_filters.NumberFilter(
        field_name="cover_date", lookup_expr="month"
    )

    class Meta:
        model = Issue
        fields = ["series_name", "series_volume", "number", "cover_year", "cover_month"]

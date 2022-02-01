import django_filters

from comicsdb.models import Issue


class IssueFilter(django_filters.FilterSet):
    cover_year = django_filters.NumberFilter(
        label="Cover Year", field_name="cover_date", lookup_expr="year"
    )
    cover_month = django_filters.NumberFilter(
        label="Cover Month", field_name="cover_date", lookup_expr="month"
    )
    publisher_name = django_filters.filters.CharFilter(
        label="Publisher Name", field_name="series__publisher__name", lookup_expr="icontains"
    )
    publisher_id = django_filters.filters.NumberFilter(
        label="Publisher Metron ID", field_name="series__publisher__id", lookup_expr="exact"
    )
    series_name = django_filters.CharFilter(
        label="Series Name", field_name="series__name", lookup_expr="icontains"
    )
    series_id = django_filters.filters.NumberFilter(
        label="Series Metron ID", field_name="series__id", lookup_expr="exact"
    )
    series_volume = django_filters.NumberFilter(
        label="Series Volume Number", field_name="series__volume", lookup_expr="exact"
    )
    store_date_range = django_filters.filters.DateFromToRangeFilter("store_date")
    series_year_began = django_filters.filters.NumberFilter(
        label="Series Beginning Year", field_name="series__year_began", lookup_expr="exact"
    )
    sku = django_filters.filters.CharFilter(
        label="Distributor SKU", field_name="sku", lookup_expr="iexact"
    )
    upc = django_filters.filters.CharFilter(
        label="UPC Code", field_name="upc", lookup_expr="iexact"
    )

    class Meta:
        model = Issue
        fields = ["number", "store_date"]

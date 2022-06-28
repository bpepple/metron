from django_filters import rest_framework as filters

from comicsdb.models import Issue


class IssueFilter(filters.FilterSet):
    cover_year = filters.NumberFilter(
        label="Cover Year", field_name="cover_date", lookup_expr="year"
    )
    cover_month = filters.NumberFilter(
        label="Cover Month", field_name="cover_date", lookup_expr="month"
    )
    publisher_name = filters.filters.CharFilter(
        label="Publisher Name", field_name="series__publisher__name", lookup_expr="icontains"
    )
    publisher_id = filters.filters.NumberFilter(
        label="Publisher Metron ID", field_name="series__publisher__id", lookup_expr="exact"
    )
    series_name = filters.CharFilter(
        label="Series Name", field_name="series__name", lookup_expr="icontains"
    )
    series_id = filters.NumberFilter(
        label="Series Metron ID", field_name="series__id", lookup_expr="exact"
    )
    series_volume = filters.NumberFilter(
        label="Series Volume Number", field_name="series__volume", lookup_expr="exact"
    )
    store_date_range = filters.DateFromToRangeFilter("store_date")
    series_year_began = filters.NumberFilter(
        label="Series Beginning Year", field_name="series__year_began", lookup_expr="exact"
    )
    sku = filters.CharFilter(label="Distributor SKU", field_name="sku", lookup_expr="iexact")
    upc = filters.CharFilter(label="UPC Code", field_name="upc", lookup_expr="iexact")

    class Meta:
        model = Issue
        fields = ["number", "store_date"]

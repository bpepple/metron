from django_filters import rest_framework as filters


class NameFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    modified_gt = filters.DateTimeFilter(
        label="Greater than Modified DateTime", field_name="modified", lookup_expr="gt"
    )

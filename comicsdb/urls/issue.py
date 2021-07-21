from django.urls import path, re_path

from comicsdb.views.issue import (
    CreatorAutocomplete,
    IssueCreate,
    IssueDelete,
    IssueDetail,
    IssueList,
    IssueUpdate,
    SearchIssueList,
    SeriesAutocomplete,
)
from comicsdb.views.variant import VariantCreate

app_name = "issue"
urlpatterns = [
    path("create/", IssueCreate.as_view(), name="create"),
    path("", IssueList.as_view(), name="list"),
    path("<slug:slug>/", IssueDetail.as_view(), name="detail"),
    path("<slug:slug>/update/", IssueUpdate.as_view(), name="update"),
    path("<slug:slug>/delete/", IssueDelete.as_view(), name="delete"),
    path("<slug:slug>/add/variant/", VariantCreate.as_view(), name="variant"),
    re_path(
        r"^creator-autocomplete/?$",
        CreatorAutocomplete.as_view(create_field="name"),
        name="creator-autocomplete",
    ),
    re_path(
        r"^series-autocomplete/?$",
        SeriesAutocomplete.as_view(),
        name="series-autocomplete",
    ),
    re_path(r"^search/?$", SearchIssueList.as_view(), name="search"),
]

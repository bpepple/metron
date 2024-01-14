from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from comicsdb.views.issue import (
    CreatorAutocomplete,
    FutureList,
    IssueCreate,
    IssueDelete,
    IssueDetail,
    IssueList,
    IssueUpdate,
    NextWeekList,
    SearchIssueList,
    SeriesAutocomplete,
    WeekList,
)

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

app_name = "issue"
urlpatterns = [
    path("create/", IssueCreate.as_view(), name="create"),
    path("", IssueList.as_view(), name="list"),
    path("<slug:slug>/", IssueDetail.as_view(), name="detail"),
    path("<slug:slug>/update/", IssueUpdate.as_view(), name="update"),
    path("<slug:slug>/delete/", IssueDelete.as_view(), name="delete"),
    path("thisweek", cache_page(CACHE_TTL)(WeekList.as_view()), name="thisweek"),
    path("nextweek", cache_page(CACHE_TTL)(NextWeekList.as_view()), name="nextweek"),
    path("future", cache_page(CACHE_TTL)(FutureList.as_view()), name="future"),
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

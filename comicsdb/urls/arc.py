from django.urls import path, re_path

from comicsdb.views.arc import (
    ArcList,
    ArcDetail,
    SearchArcList,
    ArcCreate,
    ArcUpdate,
    ArcDelete,
)


app_name = "arc"
urlpatterns = [
    path("create/", ArcCreate.as_view(), name="create"),
    path("", ArcList.as_view(), name="list"),
    path("<slug:slug>/", ArcDetail.as_view(), name="detail"),
    path("<slug:slug>/update/", ArcUpdate.as_view(), name="update"),
    path("<slug:slug>/delete/", ArcDelete.as_view(), name="delete"),
    re_path(r"^search/?$", SearchArcList.as_view(), name="search"),
]

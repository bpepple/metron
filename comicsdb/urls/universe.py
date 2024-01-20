from django.urls import path, re_path

from comicsdb.views.universe import (
    SearchUniverseList,
    UniverseCreate,
    UniverseDelete,
    UniverseDetail,
    UniverseList,
    UniverseUpdate,
)

app_name = "universe"
urlpatterns = [
    path("create/", UniverseCreate.as_view(), name="create"),
    path("", UniverseList.as_view(), name="list"),
    path("<slug:slug>/", UniverseDetail.as_view(), name="detail"),
    path("<slug:slug>/update/", UniverseUpdate.as_view(), name="update"),
    path("<slug:slug>/delete/", UniverseDelete.as_view(), name="delete"),
    re_path(r"^search/?$", SearchUniverseList.as_view(), name="search"),
]

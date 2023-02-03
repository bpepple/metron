from django.urls import include, path
from rest_framework import routers

from comicsdb.views.viewsets import (
    ArcViewSet,
    CharacterViewSet,
    CreatorViewSet,
    CreditViewset,
    IssueViewSet,
    PublisherViewSet,
    RoleViewset,
    SeriesTypeViewSet,
    SeriesViewSet,
    TeamViewSet,
    VariantViewset,
)

ROUTER = routers.DefaultRouter()
ROUTER.register("arc", ArcViewSet)
ROUTER.register("character", CharacterViewSet)
ROUTER.register("creator", CreatorViewSet)
ROUTER.register("credit", CreditViewset)
ROUTER.register("issue", IssueViewSet)
ROUTER.register("publisher", PublisherViewSet)
ROUTER.register("role", RoleViewset)
ROUTER.register("series", SeriesViewSet)
ROUTER.register("series_type", SeriesTypeViewSet)
ROUTER.register("team", TeamViewSet)
ROUTER.register("variant", VariantViewset)

app_name = "api"
urlpatterns = [path("", include(ROUTER.urls))]

from django.urls import path, include
from rest_framework import routers

from comicsdb.views.viewsets import (
    ArcViewSet,
    CharacterViewSet,
    CreatorViewSet,
    IssueViewSet,
    PublisherViewSet,
    SeriesViewSet,
    TeamViewSet,
)


ROUTER = routers.DefaultRouter()
ROUTER.register("arc", ArcViewSet)
ROUTER.register("character", CharacterViewSet)
ROUTER.register("creator", CreatorViewSet)
ROUTER.register("issue", IssueViewSet)
ROUTER.register("publisher", PublisherViewSet)
ROUTER.register("series", SeriesViewSet)
ROUTER.register("team", TeamViewSet)

app_name = "api"
urlpatterns = [path("", include(ROUTER.urls))]

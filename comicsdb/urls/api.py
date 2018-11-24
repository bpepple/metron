from django.urls import path, include
from rest_framework import routers

from comicsdb.views.viewsets import (ArcViewSet, CharacterViewSet, CreatorViewSet,
                                     PublisherViewSet, SeriesViewSet,
                                     TeamViewSet)


router = routers.DefaultRouter()
router.register('arc', ArcViewSet)
router.register('character', CharacterViewSet)
router.register('creator', CreatorViewSet)
router.register('publisher', PublisherViewSet)
router.register('series', SeriesViewSet)
router.register('team', TeamViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

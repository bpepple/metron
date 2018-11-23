from django.urls import path, include
from rest_framework import routers

from comicsdb.views.viewsets import PublisherViewSet, SeriesViewSet


router = routers.DefaultRouter()
router.register('publisher', PublisherViewSet)
router.register('series', SeriesViewSet)


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

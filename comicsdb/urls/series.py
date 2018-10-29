from django.urls import path, re_path

from comicsdb.views.series import (SeriesList, SearchSeriesList)


app_name = 'series'
urlpatterns = [
    path('page<int:page>/', SeriesList.as_view(), name='list'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$',
            SearchSeriesList.as_view(), name='search')
]

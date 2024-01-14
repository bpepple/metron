from django.urls import path
from django.views.decorators.cache import cache_page

from comicsdb.views.home import HomePageView
from comicsdb.views.statistics import statistics

app_name = ""
urlpatterns = [
    path("", cache_page(60 * 30)(HomePageView.as_view()), name="home"),
    path("statistics/", statistics, name="statistics"),
]

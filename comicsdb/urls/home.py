from django.urls import path

from comicsdb.views.home import HomePageView
from comicsdb.views.statistics import StatisticsView

app_name = ""
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
]

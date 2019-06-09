from django.urls import path

from comicsdb.views.week import WeekList


app_name = "week"
urlpatterns = [path("", WeekList.as_view(), name="list")]

from django.urls import path

from comicsdb.views.home import HomePageView


app_name = ''
urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]

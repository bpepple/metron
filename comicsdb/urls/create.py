from django.urls import path

from comicsdb.views.publisher import PublisherCreate


app_name = 'create'
urlpatterns = [
    path('publisher/', PublisherCreate, name='publisher'),
]

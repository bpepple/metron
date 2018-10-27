from django.urls import path

from comicsdb.views import PublisherList, PublisherDetail


app_name = 'publisher'
urlpatterns = [
    path('page<int:page>/', PublisherList.as_view(), name='list'),
    path('<slug:slug>/', PublisherDetail.as_view(), name='detail')
]

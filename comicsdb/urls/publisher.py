from django.urls import path, re_path

from comicsdb.views.publisher import (PublisherList, PublisherDetail,
                                      SearchPublisherList, PublisherCreate)


app_name = 'publisher'
urlpatterns = [
    path('create/', PublisherCreate.as_view(), name='create'),
    path('page<int:page>/', PublisherList.as_view(), name='list'),
    path('<slug:slug>/', PublisherDetail.as_view(), name='detail'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$',
            SearchPublisherList.as_view(), name='search')
]

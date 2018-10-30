from django.urls import path, re_path

from comicsdb.views.issue import (IssueList, IssueDetail, SearchIssueList)


app_name = 'issue'
urlpatterns = [
    path('page<int:page>/', IssueList.as_view(), name='list'),
    path('<slug:slug>/', IssueDetail.as_view(), name='detail'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$',
            SearchIssueList.as_view(), name='search')
]

from django.urls import path, re_path

from comicsdb.views.issue import (IssueList, IssueDetail, SearchIssueList,
                                  IssueCreate, IssueUpdate, IssueDelete)
from comicsdb.views.credits import CreditsCreate


app_name = 'issue'
urlpatterns = [
    path('create/', IssueCreate.as_view(), name='create'),
    path('page<int:page>/', IssueList.as_view(), name='list'),
    path('<slug:slug>/', IssueDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', IssueUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', IssueDelete.as_view(), name='delete'),
    path('<slug:slug>/add/credit/', CreditsCreate.as_view(), name='credit'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$',
            SearchIssueList.as_view(), name='search')
]

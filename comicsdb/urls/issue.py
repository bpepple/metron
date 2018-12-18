from django.urls import path, re_path

from comicsdb.views.issue import (IssueList, IssueDetail, SearchIssueList,
                                  IssueCreate, IssueUpdate, IssueDelete)
from comicsdb.views.variant import VariantCreate


app_name = 'issue'
urlpatterns = [
    path('create/', IssueCreate.as_view(), name='create'),
    path('', IssueList.as_view(), name='list'),
    path('<slug:slug>/', IssueDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', IssueUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', IssueDelete.as_view(), name='delete'),
    path('<slug:slug>/add/variant/', VariantCreate.as_view(), name='variant'),
    re_path(r'^search/?$', SearchIssueList.as_view(), name='search')
]

from django.urls import path, re_path

from comicsdb.views.team import (TeamList, TeamDetail, SearchTeamList,
                                 TeamCreate, TeamUpdate, TeamDelete)


app_name = 'team'
urlpatterns = [
    path('create/', TeamCreate.as_view(), name='create'),
    path('', TeamList.as_view(), name='list'),
    path('<slug:slug>/', TeamDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', TeamUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', TeamDelete.as_view(), name='delete'),
    re_path(r'^search/?$', SearchTeamList.as_view(), name='search')
]

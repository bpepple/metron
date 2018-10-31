from django.urls import path, re_path

from comicsdb.views.creator import (CreatorList, CreatorDetail,
                                    SearchCreatorList, CreatorCreate,
                                    CreatorUpdate, CreatorDelete)


app_name = 'creator'
urlpatterns = [
    path('create/', CreatorCreate.as_view(), name='create'),
    path('page<int:page>/', CreatorList.as_view(), name='list'),
    path('<slug:slug>/', CreatorDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', CreatorUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', CreatorDelete.as_view(), name='delete'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$',
            SearchCreatorList.as_view(), name='search')
]

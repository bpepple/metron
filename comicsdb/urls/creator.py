from django.urls import path, re_path

from comicsdb.views.creator import (CreatorList, CreatorDetail,
                                    SearchCreatorList, CreatorCreate,
                                    CreatorUpdate, CreatorDelete,
                                    CreatorSeriesList)


app_name = 'creator'
urlpatterns = [
    path('create/', CreatorCreate.as_view(), name='create'),
    path('', CreatorList.as_view(), name='list'),
    path('<slug:slug>/', CreatorDetail.as_view(), name='detail'),
    path('<slug:creator>/<slug:series>/',
         CreatorSeriesList.as_view(), name='series'),
    path('<slug:slug>/update/', CreatorUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', CreatorDelete.as_view(), name='delete'),
    re_path(r'^search/?$', SearchCreatorList.as_view(), name='search')
]

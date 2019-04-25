from django.contrib.flatpages import views
from django.urls import path


app_name = 'flatpage'
urlpatterns = [
    path('contribute/', views.flatpage,
         {'url': '/contribute/'}, name='contribute'),
    path('guidelines/editing/', views.flatpage,
         {'url': '/guidelines/editing/'}, name='editing-guidelines'),
]

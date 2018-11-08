"""metron URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from comicsdb.urls import (
    arc as arc_urls,
    character as character_urls,
    creator as creator_urls,
    issue as issue_urls,
    publisher as publisher_urls,
    series as series_urls
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('arc/', include(arc_urls)),
    path('character/', include(character_urls)),
    path('creator/', include(creator_urls)),
    path('issue/', include(issue_urls)),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('publisher/', include(publisher_urls)),
    path('series/', include(series_urls)),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

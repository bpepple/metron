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
from comicsdb.sitemaps import (
    ArcSitemap,
    CharacterSitemap,
    CreatorSitemap,
    IssueSitemap,
    PublisherSitemap,
    SeriesSitemap,
    StaticViewSitemap,
    TeamSitemap,
)
from comicsdb.urls import api as api_urls
from comicsdb.urls import arc as arc_urls
from comicsdb.urls import character as character_urls
from comicsdb.urls import contact as contact_urls
from comicsdb.urls import creator as creator_urls
from comicsdb.urls import flatpage as flatpage_urls
from comicsdb.urls import home as home_urls
from comicsdb.urls import issue as issue_urls
from comicsdb.urls import publisher as publisher_urls
from comicsdb.urls import series as series_urls
from comicsdb.urls import team as team_urls
from comicsdb.urls import week as week_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

sitemaps = {
    "arc": ArcSitemap(),
    "character": CharacterSitemap(),
    "creator": CreatorSitemap(),
    "issue": IssueSitemap(),
    "publisher": PublisherSitemap(),
    "series": SeriesSitemap(),
    "team": TeamSitemap(),
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("arc/", include(arc_urls)),
    path("character/", include(character_urls)),
    path("contact/", include(contact_urls)),
    path("creator/", include(creator_urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",
    ),
    path("", include(home_urls)),
    path("issue/", include(issue_urls)),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("pages/", include(flatpage_urls)),
    path("publisher/", include(publisher_urls)),
    path("series/", include(series_urls)),
    path("team/", include(team_urls)),
    path("accounts/", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("week/", include(week_urls)),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

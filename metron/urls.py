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
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
from comicsdb.urls import (
    api as api_urls,
    arc as arc_urls,
    character as character_urls,
    creator as creator_urls,
    flatpage as flatpage_urls,
    home as home_urls,
    issue as issue_urls,
    publisher as publisher_urls,
    series as series_urls,
    team as team_urls,
    universe as universe_urls,
)

handler404 = "metron.views.handler404"

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
    path("creator/", include(creator_urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", include(home_urls)),
    path("issue/", include(issue_urls)),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("pages/", include(flatpage_urls)),
    path("publisher/", include(publisher_urls)),
    path("select2/", include("django_select2.urls")),
    path("series/", include(series_urls)),
    path("team/", include(team_urls)),
    path("universe/", include(universe_urls)),
    path("accounts/", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
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

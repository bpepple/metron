from django.contrib.sitemaps import Sitemap

from comicsdb.models import (Arc, Character, Creator, Issue,
                             Publisher, Series, Team)


class ArcSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Arc.objects.all()

    def lastmod(self, obj):
        return obj.modified


class CharacterSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Character.objects.all()

    def lastmod(self, obj):
        return obj.modified


class CreatorSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Creator.objects.all()

    def lastmod(self, obj):
        return obj.modified


class IssueSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Issue.objects.all()

    def lastmod(self, obj):
        return obj.modified


class PublisherSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Publisher.objects.all()

    def lastmod(self, obj):
        return obj.modified


class SeriesSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Series.objects.all()

    def lastmod(self, obj):
        return obj.modified


class TeamSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Team.objects.all()

    def lastmod(self, obj):
        return obj.modified

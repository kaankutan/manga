from django.contrib.sitemaps import Sitemap
from index.models import Manga
from django.urls import reverse


class MangaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Manga.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        languages = [obj.language for obj in Manga.objects.distinct('language')]
        return languages

    def location(self, item):
        return reverse('index', kwargs={"language": item})

from django.contrib.sitemaps import Sitemap
from index.models import Manga


class MangaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Manga.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

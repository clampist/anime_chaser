from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Anime


class AnimeSitemap(Sitemap):
    changefreq = "always"
    property = 1.0
    protocol = 'https'

    def items(self):
        return Anime.objects.filter(status=Anime.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('anime-detail', args=[obj.pk])

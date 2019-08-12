"""anime_chaser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('anime/', include('anime.urls'))
"""
import xadmin

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from anime.apis import AnimeViewSet, CategoryViewSet, TagViewSet
from anime.rss import LatestAnimeFeed
from anime.sitemap import AnimeSitemap
from anime.views import (
    IndexView, CategoryView, TagView,
    AnimeDetailView, SearchView, AuthorView
)
from source.views import SourceView

from .autocomplete import CategoryAutocomplete, TagAutocomplete

router = DefaultRouter()
router.register(r'anime', AnimeViewSet, base_name='api-anime')
router.register(r'category', CategoryViewSet, base_name='api-category')
router.register(r'tag', TagViewSet, base_name='api-tag')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^anime/(?P<anime_id>\d+).html$', AnimeDetailView.as_view(), name='anime-detail'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^source/$', SourceView.as_view(), name='source'),
    url(r'^rss|feed/', LatestAnimeFeed(), name='rss'),
    url(r'^sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_')
    (sitemap_views.sitemap), {'sitemaps': {'animes': AnimeSitemap}}),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api/', include(router.urls), name='api'),
    url(r'^api/docs/', include_docs_urls(title='anime_chaser apis')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    # urlpatterns += [url(r'^silk/', include('silk.urls'), name='silk')]

from django.db.models import Q
from django.db.models import F
from datetime import date

from django.core.cache import cache

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

# from silk.profiling.profiler import silk_profile

from .models import Anime, Tag, Category


class CommonViewMixin:
    # @silk_profile(name='get_category_context')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Anime.latest_animes()
    paginate_by = 5
    context_object_name = 'anime_list'
    template_name = 'anime/list.html'


class SearchView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class CategoryView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset, 根据分类过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset, 根据分类过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class AnimeDetailView(CommonViewMixin, DetailView):
    queryset = Anime.latest_animes()
    template_name = 'anime/detail.html'
    context_object_name = 'anime'
    pk_url_kwarg = 'anime_id'

    def get(self, requset, *args, **kwargs):
        response = super().get(requset, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)

        if increase_pv and increase_uv:
            Anime.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Anime.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Anime.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

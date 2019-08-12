from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Anime, Category, Tag
from .serializers import (
    AnimeSerializer, AnimeDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    TagSerializer, TagDetailSerializer,
)


class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    anime view set
    """
    serializer_class = AnimeSerializer
    queryset = Anime.objects.filter(status=Anime.STATUS_NORMAL)
    # permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AnimeDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super().retrieve(request, *args, **kwargs)

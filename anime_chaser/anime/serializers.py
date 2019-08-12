from rest_framework import serializers, pagination

from .models import Anime, Category, Tag


class AnimeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # url = serializers.HyperlinkedIdentityField(view_name='api-anime-detail')

    class Meta:
        model = Anime
        fields = ['url', 'id', 'title', 'category', 'tag', 'owner', 'created_time']
        extra_kwargs = {
            'url': {'view_name': 'api-anime-detail'}
        }


class AnimeDetailSerializer(AnimeSerializer):
    class Meta:
        model = Anime
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time'
        )


class CategoryDetailSerializer(CategorySerializer):
    animes = serializers.SerializerMethodField('paginated_animes')

    def paginated_animes(self, obj):
        animes = obj.anime_set.filter(status=Anime.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(animes, self.context['request'])
        serializer = AnimeSerializer(page, many=True, context={'request':
                                                              self.context['request']})

        return {
            'count': animes.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time', 'animes'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'created_time'
        )


class TagDetailSerializer(TagSerializer):
    animes = serializers.SerializerMethodField('paginated_animes')

    def paginated_animes(self, obj):
        animes = obj.anime_set.filter(status=Anime.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(animes, self.context['request'])
        serializer = AnimeSerializer(page, many=True, context={'request':
                                                               self.context['request']})

        return {
            'count': animes.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'created_time', 'animes'
        )

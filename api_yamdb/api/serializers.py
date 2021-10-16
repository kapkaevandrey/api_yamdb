from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категорий"""

    class Meta:
        model = Category
        exclude = ('id',)


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанров"""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов модели Title"""
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            required=True)
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True,
                                         required=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleGetSerializer(serializers.ModelSerializer):
    """Серилализатор для GET запросов модели Title"""
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = "__all__"
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        exclude = ('title',)
        required_fields = ('score', 'text')

    def validate(self, attrs):
        request = self.context['request']
        title_id = request.parser_context['kwargs']["title_id"]
        if request.method == "PATCH":
            return attrs
        if Review.objects.filter(author=request.user,
                                 title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв к этому произведению'
            )
        return attrs


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев"""
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)

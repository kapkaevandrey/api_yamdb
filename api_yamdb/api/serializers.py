from rest_framework import serializers

from reviews.models import Category, Genre, Titles, Comment, Review


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            required=True)

    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True,
                                         required=True)

    class Meta:
        model = Titles
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        exclude = ('title',)
        required_fields = ('score',)

    # TODO пересчёт рейтинга при изменении создании отзыва
    # TODO валидация уникальности записи отдельным методом



class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев"""
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)

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
    class Meta:
        model = Titles
        fields = '__all__'

        
class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)


    class Meta:
        model = Review
        exclude = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев"""
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)

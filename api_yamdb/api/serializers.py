from rest_framework import serializers


from reviews.models import User, Review, Comment


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
        fields = "__all__"




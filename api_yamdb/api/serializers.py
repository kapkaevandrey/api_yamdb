from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, )
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Пользователя с таким именем создать невозможно',
        ),
    ])

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Данный username не разрешен, выберите другой')
        return value


class UserJwtTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Пользователя с таким именем не существует',
        ),
    ])
    confirmation_code = serializers.CharField(required=True)


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
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True)

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleGetSerializer(serializers.ModelSerializer):
    """Серилализатор для GET запросов модели Title"""
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('__all__',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(
        min_value=settings.RATING_RANGE['MIN'],
        max_value=settings.RATING_RANGE['MAX'])

    class Meta:
        model = Review
        exclude = ('title',)
        required_fields = ('score', 'text')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == "PATCH":
            return attrs
        title_id = request.parser_context['kwargs'].get("title_id")

        if Review.objects.filter(
                author=request.user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв к этому произведению')
        return attrs


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев"""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import GenresCategoryViewSet
from .filter import TitlesFilter
from .permissions import (
    AuthorAdminModeratorOrReadOnly,
    AdminOrReadOnly,
    IsAdmin)
from .serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    TitlesSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    UserJwtTokenSerializer,
    UserSerializer,
    UserSignupSerializer
)
from reviews.models import Category, Genre, Title, Review, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email').lower()
    username = serializer.validated_data.get('username')
    if User.objects.filter(email=email, username=username).exists():
        user = User.objects.get(
            email=email, username=username)
    else:
        if User.objects.filter(username=username).exists():
            return Response(f'Пользователь с username = {username}'
                            ' уже существует',
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response(f'Пользователь с email = {email} уже существует',
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    mail_subject = 'код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(mail_subject,
              message,
              settings.SERVICE_EMAIL,
              [email])
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = UserJwtTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response('Ошибка кода подтверждения',
                    status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(GenresCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(GenresCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    review = Review.objects.all()
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TitlesSerializer
        return TitleGetSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (
        AuthorAdminModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id'))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorAdminModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

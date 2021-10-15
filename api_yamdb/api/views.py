from rest_framework import viewsets, filters
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          CommentsSerializer,
                          ReviewSerializer)
from reviews.models import Category, Comment, Genre, Titles, Review
from django_filters.rest_framework import DjangoFilterBackend
from .filter import TitlesFilter
# from .permissions import CategoryGenryTitlePermissions


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    # permission_classes = (CategoryGenryTitlePermissions,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    # permission_classes = (CategoryGenryTitlePermissions,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    # permission_classes = (CategoryGenryTitlePermissions,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

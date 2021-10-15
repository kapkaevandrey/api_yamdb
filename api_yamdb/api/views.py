from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filter import TitlesFilter
from .permissions import AuthorAdminModeratorOrReadOnly
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          CommentsSerializer,
                          ReviewSerializer)
from reviews.models import Category, Comment, Genre, Titles, Review


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
    serializer_class = CommentsSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title__pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title__pk=self.kwargs.get('title_id'))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly,)
    def get_title(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return title

    def update_rating(self):
        title = self.get_title()
        reviews_number = title.reviews.count()
        if reviews_number == 0:
            title.rating = None
        else:
            current_ratio = (
                    sum(review.score for review in title.reviews.all())
                             / reviews_number)
            title.rating = int(current_ratio)
        title.save()

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
        self.update_rating()

    def perform_destroy(self, instance):
        title = self.get_title()
        instance.delete()
        self.update_rating()

    def perform_update(self, serializer):
        title = self.get_title()
        serializer.save()
        self.update_rating()


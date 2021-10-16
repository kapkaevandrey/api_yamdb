from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, filters, mixins

from .filter import TitlesFilter
from .permissions import (AuthorAdminModeratorOrReadOnly,
                          CategoryGenryTitlePermissions)
from .serializers import (CategoriesSerializer,
                          CommentsSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          ReviewSerializer,
                          TitleGetSerializer)
from reviews.models import Category, Genre, Title, Review


class GenresCategorySet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class CategoriesViewSet(GenresCategorySet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (CategoryGenryTitlePermissions,)


class GenresViewSet(GenresCategorySet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (CategoryGenryTitlePermissions,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (CategoryGenryTitlePermissions,)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesSerializer
        return TitleGetSerializer


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
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title

    def update_and_save_rating(self):
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
        self.update_and_save_rating()

    def perform_destroy(self, instance):
        title = self.get_title()
        instance.delete()
        self.update_and_save_rating()

    def perform_update(self, serializer):
        title = self.get_title()
        serializer.save()
        self.update_and_save_rating()


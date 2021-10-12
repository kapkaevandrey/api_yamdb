from rest_framework import viewsets

from .serializers import CommentsSerializer, ReviewSerializer
from reviews.models import Comment, Review


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
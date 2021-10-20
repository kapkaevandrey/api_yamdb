from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    TitlesViewSet,
    ReviewViewSet,
    UserViewSet,
    get_token,
    signup)

router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename="reviews")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename="comments")

auth = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth))
]

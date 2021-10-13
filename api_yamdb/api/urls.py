from django.db import router
from django.urls import include, path
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = SimpleRouter()

router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router.urls))]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, GetTokenViewSet, SignupViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', SignupViewSet, name='signup'),
    path('v1/auth/token/', GetTokenViewSet, name='token'),
    path('v1/', include(router.urls)),
]
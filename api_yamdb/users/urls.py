from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, get_token, signup


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/', include(router.urls)),
]
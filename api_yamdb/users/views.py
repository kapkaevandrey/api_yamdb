from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializers import (UserJwtTokenSerializer, UserSerializer,
                          UserSignupSerializer)

User = get_user_model()


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
        role = serializer.validated_data.get('role')
        if role is not None and role != user.role:
            return Response(
                {'role': 'user'},
                status=status.HTTP_200_OK)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    try:
        user, created = User.objects.get_or_create(email=email, username=username)
    except Exception as e:
        return Response({'error':str(e)},
                    status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(user)
    mail_subject = 'confirmation code'
    message = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(mail_subject,
              message,
              settings.SERVICE_EMAIL,
              [email],
              fail_silently=False)
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

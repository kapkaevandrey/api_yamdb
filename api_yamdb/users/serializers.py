from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Пользователя с таким именем создать невозможно',
        ),
    ])

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Данный username не разрешен, выберите другой')
        return value


class UserJwtTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

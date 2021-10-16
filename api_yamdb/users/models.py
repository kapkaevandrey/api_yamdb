import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields,):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        user = self.model(email=email, is_staff=True,
                          is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    choices = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]

    email = models.EmailField(
        unique=True,
    )

    bio = models.TextField(
        max_length=250,
        blank=True,
    )

    role = models.CharField(
        max_length=9,
        choices=choices,
        default='user'
    )

    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']

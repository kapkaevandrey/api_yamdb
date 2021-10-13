import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


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
    )

    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    REQUIRED_FIELDS = ['email']

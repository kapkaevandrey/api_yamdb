from functools import reduce

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  null=True,
                                  blank=True,)

    last_name = models.CharField('Фамилия',
                                 max_length=150,
                                 null=True,
                                 blank=True,)

    username = models.CharField('Имя пользователя',
                                unique=True,
                                max_length=150)

    email = models.EmailField(
        'электронная почта',
        unique=True,
        max_length=254
    )

    bio = models.TextField(
        'о себе',
        blank=True,
        null=True
    )

    role = models.CharField(
        'пользовательская роль',
        max_length=len(reduce(lambda a, b: a[1] if (
            len(a[1]) > len(b[1])) else b[1], CHOICES)),
        choices=CHOICES,
        default=USER
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

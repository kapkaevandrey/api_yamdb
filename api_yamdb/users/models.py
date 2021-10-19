from functools import reduce

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    first_name = models.CharField(
        _('first_name'),
        max_length=150,
        null=True,
        blank=True,)

    last_name = models.CharField(
        _('last_name'),
        max_length=150,
        null=True,
        blank=True,)

    username = models.CharField(
        _('username'),
        unique=True,
        max_length=150)

    email = models.EmailField(
        _('email'),
        unique=True,
        max_length=254
    )

    bio = models.TextField(
        _('bio'),
        blank=True,
        null=True
    )

    role = models.CharField(
        _('role'),
        max_length=len(reduce(lambda a, b: a[1] if (
            len(a[1]) > len(b[1])) else b[1], CHOICES)),
        choices=CHOICES,
        default=USER
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['-username']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

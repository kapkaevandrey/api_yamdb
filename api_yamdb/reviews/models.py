from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    ValidationError)
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOICES = [
        (USER, _('user')),
        (ADMIN, _('admin')),
        (MODERATOR, _('moderator')),
    ]
    first_name = models.CharField(
        _('first_name'),
        max_length=150,
        null=True,
        blank=True, )

    last_name = models.CharField(
        _('last_name'),
        max_length=150,
        null=True,
        blank=True, )

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
        max_length=len(max((role_pair[1] for role_pair in CHOICES), key=len)),
        choices=CHOICES,
        default=USER
    )

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return (
            self.is_superuser
            or self.is_staff
            or self.role == User.ADMIN)

    @property
    def is_admin_or_moderator(self):
        return self.is_admin or self.role == User.MODERATOR

    class Meta:
        ordering = ['username']
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return _('id {id} {slug}').format(id=self.id, slug=self.slug)


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return _('id {id} {slug}').format(id=self.id, slug=self.slug)


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(_('name'), max_length=50)
    year = models.PositiveSmallIntegerField(_('year'), )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('category')
    )
    description = models.TextField(_('description'), blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        verbose_name=_('genre')
    )

    def clean(self):
        if self.year > datetime.now().year:
            raise ValidationError(
                _('You cannot create a work with a date greater than '
                  '{date}').format(date=datetime.now().year)
            )

    class Meta:
        ordering = ['category__name']
        verbose_name = _('Title')
        verbose_name_plural = _('Titles')

    def __str__(self):
        return _('id - {id}, '
                 'name - {name}').format(
            id=self.id,
            name=self.name[:15])


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=_('title')
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=_('genre')
    )

    def __str__(self):
        return _('title_id - {title_id} {title_name} '
                 'genre_id - {genre_id} {slug}').format(
            title_id=self.title.id,
            title_name=self.title.name[:15],
            genre_id=self.genre.id,
            slug=self.genre.slug)


class Review(models.Model):
    """Модель отзыва на произведение."""
    text = models.TextField(_('text'))
    pub_date = models.DateTimeField(
        _('date of publication'),
        auto_now_add=True,
        db_index=True)
    score = models.PositiveSmallIntegerField(
        _('score'),
        default=1,
        validators=[
            MinValueValidator(settings.RATING_RANGE['MIN']),
            MaxValueValidator(settings.RATING_RANGE['MAX'])])
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('title')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('author')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name=_('unique review')),
        ]
        ordering = ['-pub_date']
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

    def __str__(self):
        return _('Author - {author}; title_id-{title} '
                 'review_id-{id} text part - {text}.').format(
            author=self.author,
            id=self.id,
            title=self.title.id,
            text=self.text[:15])


class Comment(models.Model):
    """Модель комментария к отзыву."""
    text = models.TextField(_('text'))
    pub_date = models.DateTimeField(
        _('date of publication'),
        auto_now_add=True,
        db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_('author')
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('review')
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return _('Author - {author}; review_id-{review_id} '
                 'comment_id-{id} text part - {text}.').format(
            author=self.author,
            id=self.id,
            review_id=self.review.id,
            text=self.text[:15])

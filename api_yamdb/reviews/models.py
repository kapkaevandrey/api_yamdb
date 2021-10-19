from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    ValidationError)
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'id {self.id} {self.slug}'


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return f'id {self.id} {self.slug}'


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
                f'Нельзя создать произведение с датой больше {datetime.now().year}'
            )

    class Meta:
        ordering = ['category__name']
        verbose_name = _('Title')
        verbose_name_plural = _('Titles')

    def __str__(self):
        return f'id - {self.id}, name - {self.name[:15]}'


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
        return (f'title_id - {self.title.id} {self.title.name[:15]}'
                f'genre_id - {self.genre_id} {self.genre.slug}')


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
                                    name='unique review'),
        ]
        ordering = ['-pub_date']
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

    def __str__(self):
        return (f'Author - {self.author}; title_id-{self.title} '
                f'review_id-{self.id} text part - {self.text[:15]}.')


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
        return (f'Author - {self.author}; review_id - {self.review_id} '
                f'comment_id - {self.id} text_part - {self.text[:15]}.')

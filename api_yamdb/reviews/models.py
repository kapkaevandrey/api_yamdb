from datetime import datetime

import django.core.exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    ValidationError)
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return f"genre_id - <{self.id}>, slug - <{self.slug}>"

    class Meta:
        ordering = ("name",)


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return f"genre_id - <{self.id}>, slug - <{self.slug}>"

    class Meta:
        ordering = ("name",)


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True)
    rating = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(settings.RATING_RANGE['MAX'])])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through="GenreTitle", blank=True)

    def clean(self):
        if self.year > datetime.now().year:
            raise ValidationError(
                f'Нельзя создать произведение с датой больше {datetime.now().year}'
            )

    def __str__(self):
        return f"title_id - <{self.id}>, name - <{self.name[:15]}>"

    class Meta:
        ordering = ['category__name']


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return (f"title_id - <{self.title.id}> <{self.title.name[:15]}>"
                f"gener_id - <{self.genre_id}> <{self.genre.slug}>")


class Review(models.Model):
    """Модель отзыва на произведение."""
    text = models.TextField()
    pub_date = models.DateTimeField('Date of publication',
                                    auto_now_add=True,
                                    db_index=True)
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(settings.RATING_RANGE['MIN']),
            MaxValueValidator(settings.RATING_RANGE['MAX'])
                    ])
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")

    def __str__(self):
        return (f'Author - <{self.author}>; title_id - <{self.title}>'
                f'review_id - <{self.id}> text part - <{self.text[:15]}>.')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique review'),
        ]
        ordering = ['-pub_date']


class Comment(models.Model):
    """Модель комментария к отзыву."""
    text = models.TextField()
    pub_date = models.DateTimeField('Date of publication',
                                    auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return (f'Author - <{self.author}>; review_id - <{self.review_id}>'
                f'comment_id - <{self.id}> text_part - <{self.text[:15]}>.')

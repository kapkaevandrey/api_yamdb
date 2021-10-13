from django.db import models
from django.core.validators import MaxValueValidator, validate_slug
from django.db.models.deletion import SET_NULL


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True, validators=[validate_slug])


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField(validators=[MaxValueValidator(2022)])
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    genry = models.ManyToManyField(Genres)
    category = models.ForeignKey(Categories, on_delete=SET_NULL, null=True)

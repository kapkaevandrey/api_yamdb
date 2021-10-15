from django_filters import rest_framework

from reviews.models import Titles


class SlugFilter(rest_framework.BaseInFilter, rest_framework.CharFilter):
    pass


class TitlesFilter(rest_framework.FilterSet):
    category = SlugFilter(field_name='category__slug', lookup_expr='in')
    genre = SlugFilter(field_name='genre__slug', lookup_expr='in')
    name = SlugFilter(field_name='name')
    year = SlugFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ['category', 'genre', 'name', 'year']

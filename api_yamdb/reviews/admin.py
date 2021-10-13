from django.contrib import admin

from .models import (Review,
                     Comment,
                     Titles,
                     Genre,
                     Category)


admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Titles)
admin.site.register(Genre)
admin.site.register(Category)
# Register your models here.

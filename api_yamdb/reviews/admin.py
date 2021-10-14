from django.contrib import admin

from .models import (Review,
                     Comment,
                     Titles,
                     Genre,
                     Category,
                     User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name',
                    'last_name', 'email', 'bio', 'role')


admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Titles)
admin.site.register(Genre)
admin.site.register(Category)

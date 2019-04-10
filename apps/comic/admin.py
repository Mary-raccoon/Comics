from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'created_at')


class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at', )

admin.site.site_header = "Comics Administration"
admin.site.register(User, UserAdmin)
admin.site.register(Comic, ComicAdmin)

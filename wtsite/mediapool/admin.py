from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'album', 'genre')

admin.site.register(Song, SongAdmin)

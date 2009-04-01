from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre')

admin.site.register(Song, SongAdmin)

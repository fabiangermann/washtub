from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    list_filter = ['artist']
    list_display = ('title', 'artist', 'album', 'genre')
    
class ArtistAdmin(admin.ModelAdmin):
    pass

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_artists', 'year')
    
class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
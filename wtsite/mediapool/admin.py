from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    list_per_page = 50  
    list_filter = ['artist']
    list_display = ('title', 'artist', 'album', 'genre')   
    list_display_links = ('title', 'artist', 'album', 'genre')
    
class ArtistAdmin(admin.ModelAdmin):
    list_per_page = 50  

class AlbumAdmin(admin.ModelAdmin):
    list_per_page = 50  
    list_display = ('name', 'artist_list', 'year')
    
class GenreAdmin(admin.ModelAdmin):
    list_per_page = 50  

admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
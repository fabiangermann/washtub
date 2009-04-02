from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_per_page = 50  
    list_filter = ['artist']
    list_display = ('title', 'artist', 'album', 'genre')
    fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('filename')
        }),
        ('Extras', {
            'fields': ('title', 'artist', 'album', 'genre', 'track', 'year', 'length', 'numplays'
                       'rating', 'lastplay', 'date_entered', 'date_modified', 'format', 'size', 
                       'description', 'comment', 'disc_count', 'disc_number', 'track_count', 'start_time',
                       'stop_time', 'eq_preset', 'relative_volume', 'sample_rate', 'bitrate', 'bpm')
        }),
    )

    
class ArtistAdmin(admin.ModelAdmin):
    list_per_page = 50  

class AlbumAdmin(admin.ModelAdmin):
    list_per_page = 50  
    list_filter = ['artist']
    list_display = ('name', 'artist_list', 'year')
    
class GenreAdmin(admin.ModelAdmin):
    list_per_page = 50  

admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
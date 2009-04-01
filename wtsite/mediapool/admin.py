from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre')
    
class ArtistAdmin(admin.ModelAdmin):
    pass    

class AlbumAdmin(admin.ModelAdmin):
    pass
    
class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Song, SongAdmin)
admin.site.register(Song, AlbumAdmin)
admin.site.register(Song, ArtistAdmin)
admin.site.register(Song, GenreAdmin)
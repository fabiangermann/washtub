from wtsite.controller.models import *
from django.contrib import admin

class ArtistInline(admin.StackedInline):
    model = Artist
    
class AlbumInline(admin.StackedInline):
    model = Album

class GenreInline(admin.StackedInline):
    model = Genre

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'album', 'genre')
    inlines = [
        ArtistInline,
    ]

class SettingAdmin(admin.ModelAdmin):
    list_filter = ['hostname']
    list_display = ('value', 'data', 'hostname')

admin.site.register(Host, HostAdmin)
admin.site.register(Setting, SettingAdmin)

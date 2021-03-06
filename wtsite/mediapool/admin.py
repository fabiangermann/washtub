#    Copyright (c) 2009, Chris Everest 
#    This file is part of Washtub.
#
#    Washtub is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Washtub is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Washtub.  If not, see <http://www.gnu.org/licenses/>.

from wtsite.mediapool.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_per_page = 100 
    list_filter = ['artist']
    list_display = ('title', 'artist', 'album', 'genre', 'date_entered')
    readonly_fields = ['filehash']
    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ('filename', 'title', 'artist', 'album', 'genre')
        }),
        ('Extras', {
            'fields': ('filehash', 'track', 'year', 'length', 'numplays',
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

class ScanResultInline(admin.StackedInline):
    model = ScanResult
    max_num = 1
    fields = ['in_progress', 'start', 'duration', 'total', 'progress', 'detail', 'songs_new', 'songs_modified', 'songs_deleted', 'artist_delta', 'album_delta', 'genre_delta', 'total_time_delta']
    readonly_fields = ['start', 'duration', 'total', 'progress', 'detail', 'songs_new', 'songs_modified', 'songs_deleted', 'artist_delta', 'album_delta', 'genre_delta', 'total_time_delta']

class MusicStatsAdmin(admin.ModelAdmin):
    list_per_page = 10
    readonly_fields = ['num_songs', 'num_artists', 'num_albums', 'num_genres', 'total_time', 'total_size', 'id']
    inlines = [
        ScanResultInline,
    ]

#class ScanResultAdmin(admin.ModelAdmin):
#    date_heirarchy = 'start'
#    list_display = ('id', 'start', 'finish', 'duration', 'in_progress', 'progress', 'detail')
#    readonly_fields = ['start', 'finish', 'current', 'total', 'detail', 'songs_new', 'songs_modified', 'songs_deleted', 'artist_delta', 'album_delta', 'genre_delta', 'total_time_delta', 'total_size_delta', 'stats_id']
#    list_per_page = 50

admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(MusicStats, MusicStatsAdmin)
##admin.site.register(ScanResult, ScanResultAdmin)

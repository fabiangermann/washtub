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

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.encoding import smart_str, smart_unicode
from os import path, access, F_OK, R_OK
import tagpy, unicodedata

def re_encode(input_string, decoder = 'utf-8', encoder = 'utf=8'):   
   try:
     output_string = unicodedata.normalize('NFD',
        input_string.decode(decoder)).encode(encoder)

   except UnicodeError:
     output_string = unicodedata.normalize('NFD', 
        input_string.decode('ascii', 'replace')).encode(encoder)
   return output_string

class Artist(models.Model):
    name = models.CharField(max_length=765)
    class Meta:
        ordering = ['name']
        db_table = u'music_artists'
    def __unicode__(self):
        return self.name

class Album(models.Model):
    artist = models.ManyToManyField(Artist)
    name = models.CharField(max_length=765)
    year = models.IntegerField(null=True)
    compilation = models.IntegerField(null=True)
    class Meta:
        ordering = ['name']
        db_table = u'music_albums'
    def __unicode__(self):
        return self.name
    def artist_list(self):
        list = self.artist.all()[:5]
        for i,l in enumerate(list):
            if i == 4:
                output += ', '+l.name+' ...'
            elif i > 0:
                output += ', '+l.name
            elif i == 0:
                output = l.name
        return output

class Genre(models.Model):
    name = models.CharField(max_length=765)
    class Meta:
        ordering = ['name']
        db_table = u'music_genres'
    def __unicode__(self):
        return self.name

class Song(models.Model):
    #filename = models.FilePathField(path=settings.MEDIAPOOL_PATH, recursive=False, match=".*(\.mp3|\.flac)$", max_length=765)
    filename = models.CharField(max_length=765)
    filehash = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=765)
    track = models.IntegerField()
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)
    genre = models.ForeignKey(Genre)
    year = models.IntegerField()
    length = models.IntegerField()
    numplays = models.IntegerField(default=0)
    rating = models.IntegerField(default=1)
    lastplay = models.DateTimeField(null=True, blank=True)
    date_entered = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    format = models.CharField(max_length=12)
    size = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=765, blank=True)
    comment = models.CharField(max_length=765, blank=True)
    disc_count = models.IntegerField(null=True, blank=True)
    disc_number = models.IntegerField(null=True, blank=True)
    track_count = models.IntegerField(null=True, blank=True)
    start_time = models.IntegerField(null=True, blank=True)
    stop_time = models.IntegerField(null=True, blank=True)
    eq_preset = models.CharField(max_length=765, blank=True)
    relative_volume = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['title']
        db_table = u'music_songs'
    def __unicode__(self):
        return self.title
        
    def save(self, force_insert=False, force_update=False):
        if type(self.filename).__name__=='unicode':
            self.filename = smart_str(self.filename)
        if not ( access(str(self.filename), (F_OK or R_OK))):
            return
        #print >>sys.stderr, "Begin:"
        try:
          ref = tagpy.FileRef(self.filename)
          tags = ref.tag()
          props = ref.audioProperties()
        except:
          #print >>sys.stderr, "Couldn't read tag: %s:" % (self.filename)
          #print >>sys.stderr, "Unexpected error:", sys.exc_info()[0]
          return
        #print >>sys.stderr, "End tagpy FileRef:"
 
        #take care of the non-relational fields first
        self.title = tags.title     
        self.year = tags.year
        self.length = props.length
        self.sample_rate = props.sampleRate
        self.bitrate = props.bitrate
        ext = path.splitext(self.filename)
        self.format = ext[len(ext)-1]
        if not (tags.track):
            self.track = 1
        else:
            self.track = tags.track
    
        # now take care of ForeignKeys
        a, created = Artist.objects.get_or_create(name=tags.artist)
        if(created):
            self.artist = a
        else:
            self.artist = a
        
        try:
            b = Album.objects.get(name=tags.album, artist=a)
            self.album = b
        except Album.DoesNotExist:
            try:
                b = Album.objects.get(name=tags.album)
                b.artist.add(a)
                b.save()
            except Album.DoesNotExist:
                b = Album.objects.create(name=tags.album)
                b.artist.add(a)
                b.save()
        self.album = b
        
        created = False
        a, created = Genre.objects.get_or_create(name=tags.genre)
        if(created):
            self.genre = a
        else:
            self.genre = a
        #Finally, re_encode the filename to make sure it can convert to unicode
        try:
            self.filename = smart_unicode(self.filename)
        except:
            self.filename = re_encode(self.filename)
            self.filename = smart_unicode(self.filename)
            test_val = self.filename
        super(Song, self).save(force_insert, force_update)
        

class Albumart(models.Model):
    filename = models.FilePathField(path=settings.MEDIAPOOL_PATH, recursive=True, max_length=765)
    #directory = models.ForeignKey(Directory)
    imagetype = models.IntegerField()
    song = models.ForeignKey(Song)
    embedded = models.IntegerField()
    class Meta:
        db_table = u'music_albumart'

class Playlists(models.Model):
    name = models.CharField(max_length=765)
    songs = models.TextField()
    last_accessed = models.DateTimeField()
    length = models.IntegerField()
    songcount = models.IntegerField()
    hostname = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_playlists'

class SmartplaylistCategories(models.Model):
    name = models.CharField(max_length=384)
    class Meta:
        db_table = u'music_smartplaylist_categories'

class SmartplaylistItems(models.Model):
    smartplaylistid = models.IntegerField()
    field = models.CharField(max_length=150)
    operator = models.CharField(max_length=60)
    value1 = models.CharField(max_length=765)
    value2 = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_smartplaylist_items'

class Smartplaylists(models.Model):
    name = models.CharField(max_length=384)
    categoryid = models.IntegerField()
    matchtype = models.CharField(max_length=21)
    orderby = models.CharField(max_length=384)
    limitto = models.IntegerField()
    class Meta:
        db_table = u'music_smartplaylists'

class MusicStats(models.Model):
    num_artists = models.IntegerField(default=0)
    num_albums = models.IntegerField(default=0)
    num_songs = models.IntegerField(default=0)
    num_genres = models.IntegerField(default=0)
    total_time = models.CharField(default=0,max_length=36)
    total_size = models.CharField(default=0,max_length=30)
    class Meta:
        db_table = u'music_stats'
        verbose_name_plural = 'Music Stats'
    def __unicode__(self):
        return u'%d' % self.id
    def calculate(self):
        self.num_artists = Artist.objects.count()
        self.num_albums = Album.objects.count()
        self.num_songs = Song.objects.count()
        self.num_genres = Genre.objects.count()
        t = Song.objects.aggregate(time=Sum('length'), size=Sum('size'))
        if t['time'] is not None:
            self.total_time = t['time']
        if t['size'] is not None:
            self.total_size = t['size']
        super(MusicStats, self).save()

class ScanResult(models.Model):
    start = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    finish = models.DateTimeField(auto_now=True, null=False, blank=False)
    current = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    detail = models.CharField(max_length=765)
    in_progress = models.BooleanField()
    songs_new = models.IntegerField(default=0)
    songs_modified = models.IntegerField(default=0)
    songs_deleted = models.IntegerField(default=0)
    artist_delta = models.IntegerField(default=0)
    album_delta = models.IntegerField(default=0)
    genre_delta = models.IntegerField(default=0)
    total_time_delta = models.BigIntegerField(default=0)
    total_size_delta = models.BigIntegerField(default=0)
    stats_id = models.ForeignKey(MusicStats)
    class Meta:
        db_table = u'music_scan_result'
    def __unicode__(self):
        return u'%d' % self.id
    def duration(self):
        return (self.finish - self.start)
    def progress(self):
        try:
            return int((float(self.current)/float(self.total)) * 100)
        except ZeroDivisionError:
            return 0
    def calculate_delta(self, previous_scan_id):
        if previous_scan_id != -1: # Then this is NOT the first scan and we can continue
            old_stats = MusicStats.objects.get(scanresult__id__exact=previous_scan_id)
            new_stats = MusicStats.objects.get(scanresult__id__exact=self.id)
            empty = MusicStats.objects.none()
            if old_stats == empty or new_stats == empty: # Then bail, something is wrong
                return
            self.artist_delta = int(new_stats.num_artists) - int(old_stats.num_artists)
            self.album_delta = int(new_stats.num_albums) - int(old_stats.num_albums)
            self.genre_delta = int(new_stats.num_genres) - int(old_stats.num_genres)
            self.total_time_delta = int(new_stats.total_time) - int(old_stats.total_time)
            self.total_size_delta = int(new_stats.total_size) - int(old_stats.total_size)
            super(ScanResult, self).save()
        else:
            # This is the first scan 'EVAR' and we can bail out and leave the deltas NULL
            return

    def save(self, force_insert=False, force_update=False):
        # Create a new instance of MusicStats
        try:
            if self.stats_id == None:
               pass 
        except:
            m = MusicStats()
            m.save()
            self.stats_id = m
        super(ScanResult, self).save(force_insert, force_update)

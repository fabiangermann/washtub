from django.db import models
from django.conf import settings
from os import path, access, stat, F_OK, R_OK
import tagpy  

#class Directory(models.Model):
#    path = models.TextField()
#    parent_id = models.IntegerField()
#    class Meta:
#        db_table = u'music_directories'

class Artist(models.Model):
    name = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_artists'

class Album(models.Model):
    artist = models.ForeignKey(Artist)
    name = models.CharField(max_length=765)
    year = models.IntegerField()
    compilation = models.IntegerField()
    class Meta:
        db_table = u'music_albums'

class Genre(models.Model):
    genre = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_genres'

class Song(models.Model):
    filename = models.FilePathField(path=settings.MEDIAPOOL_PATH, recursive=True, max_length=765)
    title = models.CharField(max_length=765)
    track = models.IntegerField()
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)
    genre = models.ForeignKey(Genre)
    year = models.IntegerField()
    length = models.IntegerField()
    numplays = models.IntegerField()
    rating = models.IntegerField()
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
        db_table = u'music_songs'
        
    def save(self, force_insert=False, force_update=False):
        if not ( access(self.filename, (F_OK or R_OK))):
            return
        ref = tagpy.FileRef(self.filename)
        tags = ref.tag()
        props = ref.audioProperties()
        
        #take care of the non-relational field first
        if not (self.title):
            self.title = tags.title
        if not (self.year):
            self.year = tags.year
        if not (self.track):
            if not (tags.track):
                self.track = 1
            else:
                self.track = tags.track
        if not (self.length):
            self.length = props.length
        if not (self.sample_rate):
            self.sample_rate = props.sampleRate
        if not (self.bitrate):
            self.bitrate = props.bitrate
        if not (self.format):
            ext = path.splitext(self.filename)
            self.format = ext[len(ext)-1]
        
        # now take care of ForeignKeys
        if not (self.artist):
            try:
                a = Artist.objects.get(name=tags.artist)
            except Artist.DoesNotExist:
                a = Artist.objects.create(name=tags.artist)
            self.artist = a
        if not (self.album):
            a = Album.objects.get(name=tags.album)
            if not (a):
                a = Album.objects.create(name=tags.album)
            self.album = a
        if not (self.genre):
            a = Genre.object.get(name=tags.genre)
            if not (a):
                a = Genre.objects.create(name=tags.genre)
            self.genre = a
             
            
        super(Blog, self).save(force_insert, force_update)
        

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
    num_artists = models.IntegerField()
    num_albums = models.IntegerField()
    num_songs = models.IntegerField()
    num_genres = models.IntegerField()
    total_time = models.CharField(max_length=36)
    total_size = models.CharField(max_length=30)
    class Meta:
        db_table = u'music_stats'

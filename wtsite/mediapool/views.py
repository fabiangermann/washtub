from django.conf import settings
from wtsite.mediapool.models import *
from os import path, access, stat, walk, F_OK, R_OK
from os.path import join, getsize
import tagpy

# Create your views here.
def add_file(file):
    s = Song(filename=file)
    s.save()

def build_file_list(dir, queries, parent_id):
    if not (access(dir, (F_OK or R_OK))):
        return
    list = walk(dir,topdown=True)
    for root, dirs, files in list:
        for f in files:
            ext = path.splitext(f)
            assert False
            if ext in ('.mp3', 'flac'):
                full_path = path.join(root,f)
                if (f in queries['songs'].filter(filename=full_path)):
                    #check update time and compare against database.
                    pass
                else:
                    #add it into the database
                    add_file(full_path)

def file_scanner(request):
    queries = {}

    #setup queryset for Directories
    #dirs = Directory.objects.all()
    #queries['dirs'] = dirs
    
    #setup queryset for Genres
    genres = Genre.objects.all()
    queries['genres'] = genres
    
    #setup queryset for Artists
    artists = Artist.objects.all()
    queries['artists'] = artists
    
    #setup queryset for Albums
    albums = Album.objects.all()
    queries['albums'] = albums
    
    #setup queryset for Songs
    songs = Song.objects.all()
    queries['songs'] = songs
    
    if(settings.MEDIAPOOL_PATH):
        directory = settings.MEDIAPOOL_PATH
    else:
        return
    
    build_file_list(directory, queries, 0)
    
    return

    
    
    
    
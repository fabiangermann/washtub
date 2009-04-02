from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from wtsite.mediapool.models import *
from os import path, access, stat, walk, F_OK, R_OK
from os.path import join, getsize
from os.stat import ST_MTIME
import tagpy, datetime 

def build_file_list(dir, queries, parent_id):
    if not (access(dir, (F_OK or R_OK))):
        return
    list = walk(dir,topdown=True)
    for root, dirs, files in list:
        for f in files:
            ext = path.splitext(f)[1]
            if ext in ('.mp3', 'flac'):
                full_path = path.join(root,f)
                mod_time = stat(full_apath)[ST_MTIME]
                if (f in queries['songs'].filter(filename=full_path)):
                    #check update time and compare against database.
                    s = queries['songs'].filter(filename=full_path)
                    if(mod_time > s.date_modified):
                        s = Song(filename=file, date_modified=mod_time)
                        s.save()
                else:
                    #add it into the database
                    s = Song(filename=file, date_modified=mod_time, date_entered= datetime.now)
                    s.save()
    
    return

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
    
    return HttpResponseRedirect('/washtub/')
    
    
    
    
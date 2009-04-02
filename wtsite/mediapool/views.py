from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from wtsite.mediapool.models import *
from os import access, stat, path, walk, F_OK, R_OK
from os.path import join, getsize
from stat import ST_MTIME
import tagpy, datetime 

def build_file_list(dir, queries):
    if not (access(dir, (F_OK or R_OK))):
        return
    list = walk(dir,topdown=True)
    for root, dirs, files in list:
        for f in files:
            ext = path.splitext(f)[1]
            if ext in ('.mp3', 'flac'):
                full_path = path.join(root,f)
                mod_time = datetime.fromtimestamp(stat(full_path)[ST_MTIME]).isoformat()
                if (f in queries['songs'].filter(filename=full_path)):
                    #check update time and compare against database.
                    s = queries['songs'].filter(filename=full_path)
                    if(mod_time > s.date_modified):
                        s = Song(filename=file, date_modified=mod_time)
                        s.save()
                else:
                    #add it into the database
                    now = datetime.datetime.now().isoformat()
                    s = Song(filename=file, date_modified=mod_time, date_entered=now)
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
    
    build_file_list(directory, queries)
    
    return HttpResponseRedirect('/washtub/')
    
    
    
    
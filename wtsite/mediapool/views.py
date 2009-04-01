from django.conf import settings
from wtsite.mediapool import models
from os import path, access, stat, walk

# Create your views here.
def build_file_list(dir, queries, parent_id):
    if not (access(dir, F_OK, R_OK)):
        return
    list = walk(dir,topdown=True)
    assert False

def file_scanner(request):
    queries = {}

    #setup queryset for Directories
    dirs = Directory.get.objects.all()
    queries[dirs] = dirs
    
    #setup queryset for Genres
    genres = Genre.get.objects.all()
    queries[genres] = dirs
    
    #setup queryset for Artists
    artists = Artist.get.objects.all()
    queries[artists] = dirs
    
    #setup queryset for Albums
    albums = Album.get.objects.all()
    queries[albums] = dirs
    
    #setup queryset for Songs
    songs = Song.get.objects.all()
    queries[songs] = dirs
    
    if(settings.MEDIAPOOL_PATH):
        directory = settings.MEDIAPOOL_PATH
    else:
        return
    
    build_file_list(directory, queries, parent_id)
    
    return

    
    
    
    
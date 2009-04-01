from django.conf import settings
from wtsite.mediapool.models import *
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
    dirs = Directory.objects.all()
    queries[dirs] = dirs
    
    #setup queryset for Genres
    genres = Genre.objects.all()
    queries[genres] = dirs
    
    #setup queryset for Artists
    artists = Artist.objects.all()
    queries[artists] = dirs
    
    #setup queryset for Albums
    albums = Album.objects.all()
    queries[albums] = dirs
    
    #setup queryset for Songs
    songs = Song.objects.all()
    queries[songs] = dirs
    
    if(settings.MEDIAPOOL_PATH):
        directory = settings.MEDIAPOOL_PATH
    else:
        return
    
    build_file_list(directory, queries, 0)
    
    return

    
    
    
    
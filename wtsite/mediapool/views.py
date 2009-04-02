from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.decorators import login_required
from wtsite.mediapool.models import *
from os import access, stat, path, walk, F_OK, R_OK
from os.path import join, getsize
from stat import ST_MTIME
import tagpy, datetime 

def build_file_list(dir):
    if not (access(dir, (F_OK or R_OK))):
        return
    list = walk(dir,topdown=True)
    for root, dirs, files in list:
        for f in files:
            ext = path.splitext(f)[1]
            if ext in ('.mp3', 'flac'):
                full_path = path.join(root,f)
                mod_time = stat(full_path)[ST_MTIME]
                mod_time = datetime.datetime.fromtimestamp(mod_time)
                try: 
                    #check update time and compare against database.
                    s = Song.objects.get(filename=full_path)
                    if(mod_time > s.date_modified): 
                        s.date_modified=mod_time.isoformat(' ')
                        s.save()
                    return
                except Song.DoesNotExist:
                    #add it into the database
                    now = datetime.datetime.now().isoformat(' ')
                    s = Song(filename=full_path, date_modified=mod_time, date_entered=now)
                    s.save()
    return

def clean_db(dir, songs):
    if not (access(dir, (F_OK or R_OK))):
        return
    list = walk(dir,topdown=True)
    for s in songs:
        found = False
        db_filename = smart_str(s.filename)
        for root, dirs, files in list:
            if(found):
                continue
            for f in files:
                if(found):
                    continue
                ext = path.splitext(f)[1]
                if ext in ('.mp3', '.flac'):
                    full_path = path.join(root,f)
                    if(full_path == '/mnt/nfs/lx-gateway/data/audio/washtub/Aeroc/Viscous Solid/12-Another Mere Moment-Aeroc-Viscous Solid-320kbps.mp3'):
                        assert False
                    if(full_path == db_filename):
                        found = True
                        continue
        if not found:
            d = Song.objects.get(filename__exact=s.filename)
            assert False
            d.delete()
    return  

@login_required()
def file_scanner(request):
    
    if(settings.MEDIAPOOL_PATH):
        directory = settings.MEDIAPOOL_PATH
    else:
        return
    
    list = build_file_list(directory)
    songs = Song.objects.all()
    clean_db(directory, songs)
    
    return HttpResponseRedirect('/washtub/')
    
    
    
    
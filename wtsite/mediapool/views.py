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

from time import sleep
from django.forms import model_to_dict
from django.conf import settings
from django.core.paginator import Paginator
from django.utils import simplejson
from django.core import serializers
from django.http import HttpResponseForbidden, Http404, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.utils.encoding import smart_str, smart_unicode
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from wtsite.mediapool.models import *
from os import access, stat, path, walk, F_OK, R_OK
from os.path import join, getsize
from stat import ST_MTIME, ST_SIZE
import sys, hashlib, tagpy, datetime, logging, re, time, mimetypes

def stream(request, hash_id):
  # One all inclusive streaming view to auth and stream files
  # Protect streaming items in mediapool from cross-site serving
  s = get_object_or_404(Song, filehash=hash_id)

  # If GET request, then we are serving a stream.
  # To serve a stream, we require a stream token in the current session to match the item.
  # Once, we use the stream token it's removed, preventing the user from manually downloading the item.
  if request.method == 'GET':
    auth = False
    if 'stream_token' in request.session.keys():
      # Clear out expired tokens for this session
      for t, expires in request.session['stream_token'].copy().iteritems():
        if datetime.datetime.now() > expires:
          del request.session['stream_token'][t]
          request.session.modified = True
          print >>sys.stderr, 'Expired token removed: %s' % t
      t = get_token(s.id)
      #print >>sys.stderr, ('GET: stream_token: %s, song_token: %s' % (request.session['stream_token'], t))
      if t in request.session['stream_token']:
        auth = True
        print >>sys.stderr, 'Auth == True, removing token for media protection'
        del request.session['stream_token'][t]
        request.session.modified = True # We must force the modified attr since we modified the token_list
    if not auth:
      response = HttpResponse('Forbidden')
      response.status_code = 403
      return response
    response = HttpResponse() # 200 OK

    # Grab and send 'Range' header for use with X-Sendfile
    if 'HTTP_RANGE' in request:
      response['Range'] = request['HTTP_RANGE']
    #print >>sys.stderr, request
    mimetype = mimetypes.guess_type(s.filename)[0]
    response['Content-Type'] = mimetype # Try to determine the mimetype, shouldn't be text/plain; charset=UTF-8
    print >>sys.stderr, 'Sending File: %s' % smart_str(s.filename, encoding='utf-8')
    response['X-Sendfile'] = smart_str(s.filename)
    response['Cache-Control'] = 'no-cache'
    response['Accept-Ranges'] = 'bytes'
    print >>sys.stderr, response
    return response

  # If POST request, then we are requesting auth to stream an item
  # To auth a stream, we require a csrf token. Preferably SSL to prevent cross-site POSTS.
  # Once a valid POST is received, a stream token is added to the session for the item requested
  if request.method == 'POST':
    expires = datetime.datetime.now() + datetime.timedelta(seconds=+(s.length + 10))
    print >>sys.stderr, "new token created. expires: %s" % expires
    t = get_token(s.id)
    if 'stream_token' not in request.session.keys():
      request.session['stream_token'] = {}
    request.session['stream_token'][t] = expires
    request.session.modified = True # We must force the modified attr since we modified the token_list
    print >>sys.stderr, ('POST: stream_token: %s, song_token: %s' % (request.session['stream_token'], t))
    return HttpResponse("OK")
  else:
    response = HttpResponse()
    response.status_code = 403
    return response

def stream_test(request, hash_id):
  s = get_object_or_404(Song, filehash=hash_id)
  return render_to_response('stream_test.html', {'song': s}, context_instance=RequestContext(request))

def stream_test_liq(request):
  return render_to_response('stream_test_liq.html', {}, context_instance=RequestContext(request))

def get_token(song_id):
    # Create a new stream token
    t = hashlib.new('ripemd160')
    t.update("%s%s" % (song_id, settings.MEDIAPOOL_KEY))
    return t.hexdigest()

def get_file_hash(filename):
  filehash = '0'
  initialsize = stat(filename)[ST_SIZE]
  readcount = 65536

  if initialsize < readcount*2:
    print >>sys.stderr, 'file is too small to hash'
    return ''

  if access(filename, R_OK):
    filehash = str(initialsize)
  else:
    print >>sys.stderr, 'file is not readablei for hashing'
    return ''

  progress = 0
  # Read the beginning of the file
  with open(filename, "rb") as f:
    f.seek(0)
    byte = f.read(1)
    while byte and progress < readcount:
      # Do stuff with byte.
      byte = f.read(1)
      filehash += byte
      progress += 1

  progress = 0
  # Read the tail of the file
  with open(filename, "rb") as f:
    f.seek(initialsize - readcount)
    byte = f.read(1)
    while byte and progress < readcount:
      # Do stuff with byte.
      byte = f.read(1)
      filehash += byte
      progress += 1

  # Create a hash from the bytes we read
  t = hashlib.new('ripemd160')
  t.update("%s%s" % (filehash, settings.MEDIAPOOL_KEY))
  return t.hexdigest()
  
def build_file_list(directory, r):
    logging.info('Start of build_file_list(%s)' % directory)
    if not (access(directory, (F_OK or R_OK))):
        return False
    
    walk_cache = walk(directory,topdown=True)
    # Setup our scan statistics
    current = 0
    total = 0
    new = 0
    modified = 0
    file_list = []

    # Compile the list first, so we can get some stats
    for root, dirs, files in walk_cache:
        for f in files:
            if re.search('\.(mp3|flac)$', f, re.I):
                file_list.append(path.join(root,f))
                total = total + 1

    # Start the scan results record for progress metering
    r.total = total
    r.in_progress = True
    r.save()
    
    # Create a reasonable progress checkpoint based on a fraction of the total
    # We don't want to update progress on every pass of the scan loop
    progress_mod = int(total/150)
    logging.info('Finish walk of (%s)' % directory)
    for i, full_path in enumerate(file_list):
        statinfo = stat(full_path)
        if statinfo[ST_SIZE] == 0:
          continue
        mod_time = statinfo[ST_MTIME]
        mod_time = datetime.datetime.fromtimestamp(mod_time)
        try: 
            # check update time and compare against database.
            s = Song.objects.get(filename=full_path)

            # Uncomment and run me once:
            # Update size for every existing filename path
            #s.size = statinfo[ST_SIZE]
            #s.save()
            #print >>sys.stderr, "Applying size: %s, id: %s, filename: %s" % (statinfo[ST_SIZE], s.id, full_path)

            # XXX: Update file hashes for songs that exist, but haven't been hashed yet
            # This could facilitate upgrades and should be a onetime thing

            if(mod_time > s.date_modified):
                modified = modified + 1
                fhash = get_file_hash(full_path)
                mod_time = stat(full_path)[ST_MTIME]
                mod_time = datetime.datetime.fromtimestamp(mod_time)
                s.date_modified = mod_time.isoformat(' ')
                s.size = statinfo[ST_SIZE]
                s.filehash = fhash
                s.save()
        except Song.DoesNotExist:
            #add it into the database
            new = new + 1
            fhash = get_file_hash(full_path)
            #print >>sys.stderr, 'retrieved hash: %s for %s' % (fhash, full_path) 
            mod_time = mod_time.isoformat(' ')
            now = datetime.datetime.now().isoformat(' ')
            s = Song(filename=full_path, date_modified=mod_time, date_entered=now, filehash=fhash, size=statinfo[ST_SIZE])
            s.save()
        current = current + 1
        if ((current % progress_mod) == 0 or i == (len(file_list) - 1)):
            #sleep(.05)
            r.songs_new = new
            r.songs_modified = modified
            r.current = current
            r.save()
    logging.info('End of build_file_list(%s)' % directory)
    return True

def clean_db(directory, songs, r):
    logging.info('Start of clean_db(%s)' % directory)
    if not (access(directory, (F_OK or R_OK))):
        return False

    # remove songs that are in the database, but aren't physically on the filesystem
    deleted = 0
    for s in songs:
        filename = smart_str(s.filename)
        if not (access(filename, (F_OK or R_OK))):
            # Check to see if the hash exists in any of the new records
            # If so, then file was moved
            results = Song.objects.filter(filehash=s.filehash).exclude(filename=filename)
            if results:
              for n in results:
                print >>sys.stderr, "Song hash exists, file moved: %s, %s" % (s.filehash, filename)
                # Retain old record to persist the id and stats
                # assign new filename to old record, delete new virgin record
                s.filename = n.filename
                s.save()
                n.delete()
            else:
              s.delete()
              deleted = deleted + 1
    
    # refresh list of songs (we may have just deleted some)
    songs = Song.objects.all()
    # remove albums that don't have corresponding songs
    for t in (Album, Artist, Genre):
        d = t.objects.filter(song__title__isnull=True)
        d.delete()

    # Save the latest scan results
    r.songs_deleted = deleted
    r.save()

    # Calculate our new mediapool stats after all the work is done
    new_stats = MusicStats.objects.get(scanresult=r.id)
    new_stats.calculate()
    
    logging.info('End of clean_db(%s)' % directory)
    return True

@login_required()
def file_scanner(request):
  json = {}
  if request.method == 'POST':    
    if(settings.MEDIAPOOL_PATH):
        directory = settings.MEDIAPOOL_PATH
    else:
        return False
 
    # Check to see if there is a current scan in progress.
    if ScanResult.objects.filter(in_progress=True).exists():
        # Catch this and return a useful message
        return HttpResponseServerError

    # Empty all songs from current database.  This should be fast!!!
    #for t in (Artist, Album, Genre, Song, Albumart):
    #  d = t.objects.all()
    #  d.delete()

    # Get the latest previous ScanResult before we do anything
    # so we can generate stats after the new scan is run
    ms = ScanResult.objects.order_by('-id')
    if ms.exists():
      scan_id = ms[0].id
    else:
      scan_id = -1

    # Create a new scan result row
    r = ScanResult(current=0,total=0,in_progress=False)
    r.save()
    status = build_file_list(directory, r)
    if status: # don't keep going, stop and return and error msg to the caller
      songs = Song.objects.all()
      status = clean_db(directory, songs, r)

      # Finally, generate the deltas from the last scan to this one
      r.calculate_delta(scan_id)

      # Close out the scan in progress.  Not sure how this will work for a pidlock-esque situation    
      r.in_progress = False
      r.save()
      sleep(6)
    # Construct our status message
    if status:
      json['type'] = 'info'
      json['msg'] = 'Complete'
    else:
      json['type'] = 'error'
      json['msg'] = 'something went wrong'
  else:
    #return message about Get with bad parameters.
    json['type'] = 'error'
    json['msg'] = 'Media scan cannot be initiated via GET requests.'
  return HttpResponse(simplejson.dumps(json), mimetype='application/json')

def scanner_status(request):
  json = {}
  s = ScanResult.objects.filter(in_progress__exact=True)
  if s.exists():
    if s.count() == 1:
      json['type'] = 'info'
      json['msg'] = 'OK'
      json['scan_status'] = [model_to_dict(e) for e in s] #serializers.serialize('json', list(s), ensure_ascii=False) 
      json['progress'] = [e.progress() for e in s]
      json['duration'] = [e.duration().total_seconds() for e in s]
      dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
      json = simplejson.dumps(json, indent=2, ensure_ascii=False, default=dthandler)
      return HttpResponse(json, mimetype='application/json')
    elif s.count > 1:
      json['type'] = 'error'
      json['msg'] = 'There seems to be more than one scan in progress.  That should not happen.'
  else:
    json['type'] = 'error'
    json['msg'] = 'There are no scans currently in progress.'
  return HttpResponse(simplejson.dumps(json), mimetype='application/json')

def get_song_pager():
	 pager = Paginator(Song.objects.all(), 15)
	 return pager

def get_song_search_pager(queryset):
     pager = Paginator(queryset, 15)
     return pager

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

from django.conf import settings
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.http import QueryDict
from django.db.models import Q
from django.template import RequestContext
from wtsite.controller.models import *
from wtsite.controller.templatetags.controller_extras import *
from wtsite.mediapool.models import *
from wtsite.mediapool.views import *
import telnetlib, string, time, datetime, threading, re
from datetime import datetime
from threading import Thread


############################################################################
#	Begin 'Utility' Functions
#	These are discrete utilities that interact with the liquidsoap server  
#	These are not called directly by urls.py
############################################################################
def is_online(host, host_settings):
	port = None
	for p in host_settings:
	   if p.value == 'port':
	       port = str(p.data)
	#default port number (for telnet)
	if not port:
		port = '1234' 
	command='help\n'
	try:
		tn = telnetlib.Telnet(str(host.ip_address), port, 2)
		tn.write(command)
		response = tn.read_until("END")
		tn.close()
		response = True
	except:
		response = False
	return response
	
def parse_command(host, host_settings, command):
  port = None
  for p in host_settings:
     if p.value == 'port':
         port = str(p.data)
  #default port number (for telnet)
  if not port:
    port = '1234' 
  command+='\n'
  try:
    tn = telnetlib.Telnet(str(host.ip_address), port)
    tn.write(str(command))
    response = tn.read_until("END")
    tn.write('quit\n')
    tn.close()
  except:
    raise Exception() # This exception needs to be caught and sent to users
  response = re.sub('\nEND$', '', response)
  response = response.rstrip()
  return response

def parse_metadata(host, host_settings, rid):
        v = Version.objects.get(host__version__exact=host.version)
        if v.version == '0.9.x':
		command = 'metadata'
        else:
                command = 'request.metadata'
	meta_list = parse_command(host, host_settings, '%s %s' % (command, rid))
	meta_list = meta_list.splitlines()
	metadata = {}
	for m in meta_list:
		m = m.split('=')
		if len(m) > 1:
			if m[0] != 'END':
				if m[0] == 'on_air':
					datestring = m[1].strip('"')
					mydate = datetime.strptime(datestring, "%Y/%m/%d %H:%M:%S")
					metadata[m[0]] = mydate
				else:
					metadata[m[0]] = m[1].strip('"')
	return metadata

def parse_queue_metadata(host, host_settings, queue, storage):
	if not storage:
	   storage = {}
	if queue:
		for name,entries in queue.iteritems():
			for rid in entries['rids']:
				if rid not in storage:
					storage[rid]= parse_metadata(host, host_settings, rid)
	return storage

def parse_node_list(host, host_settings):
	list = parse_command(host, host_settings, "list")
	list = list.splitlines()
	out = {}
	for item in list:
		if item != 'END':
			item = item.split(' : ')
			out[item[0]]=item[1]
	return out

def parse_var_list(host, host_settings):
  list = parse_command(host, host_settings, "var.list")
  list = list.splitlines()
  out = {}
  for item in list:
    if item != 'END':
      item = item.split(' : ')
      fullname = item[0]
      varname = fullname.split('_')
      vartype = item[1]
      if len(varname) > 1:
        scope = varname[0]
        name = varname[1]
      else:
        scope = 'global'
        name = varname[0]
      # Let's get the variable value while we are here
      value = parse_command(host, host_settings, "var.get %s" % (fullname))
      # Liquidsoap interactive variables can either be string or float
      if vartype == 'float':
        value = float(value)
      else:
        value = str(value)
      out[scope] = {name: {'type': vartype, 'value': value } }
  return out

def parse_help(host, host_settings):
	list = parse_command(host, host_settings, "help")
	list = list.splitlines()
	out = []
	for item in list:
		if item.startswith('|'):
			item = item.lstrip('| ')
			out.append(item)
	list = out
	return list

def parse_rid_list(host, host_settings, command):
	entry = parse_command(host, host_settings, command)
	entry = entry.split()
	entry_list = []
	for e in entry:
		if e != 'END':
		 entry_list.append(e)
	return entry_list

def parse_output_streams(host, host_settings, node_list):
	streams = []
	for node,type in node_list.iteritems():
		temp = type.split('.')
		if ('output' in temp):
			streams.append(node)
	return streams

def parse_input_streams(host, host_settings, node_list):
	streams = []
	for node,type in node_list.iteritems():
		if (type == 'input.http'):
			streams.append(node)
	return streams
							
def parse_history(host, host_settings, node_list):
	history = {}
	for node,type in node_list.iteritems():
		type = type.split('.')
		if (len(type) > 0):
			if ('output' in type):
				entry_list = []
				meta = parse_command(host, host_settings, '%s.metadata\n' % (node))
				meta = meta.splitlines()
				for line in meta:
					line = line.split('=')
					if( 'rid' in line):
						if ( len(line) > 1 ):
							entry_list.append(line[1].strip('"'))
				found = False
				for name,list in history.copy().iteritems():
					if(list == entry_list):
					   found = True
					   new_name = name+', '+node
                                           history[new_name] = {}
					   history[new_name]['rids'] = entry_list
					   del history[name]
				if(not found):
                                        history[node] = {}
					history[node]['rids'] = entry_list
	return history
  
def parse_queue_dict(host, host_settings):
	queue_list = []
	for s in host_settings:
	   if s.value == 'queue_id':
	   	queue_list.append(str(s.data))
	if queue_list == []:
		return None
	request_list = {}
	for q in queue_list:
          request_list[q] = {}
          
          # Determine the type of queue we're dealing with
          cmd = '%s.pending_length' % (q)
          response = parse_command(host, host_settings, cmd)
          if (re.match('ERROR', response)):
            # queue is not editable
            q_type = 'queue'
          else:
            q_type = 'equeue'
            request_list[q]['pending_length'] = response
          request_list[q]['type'] = q_type  
          
          # Determine the queue_offset, This is basically the length of the queue - pending_length.
          # Or how many things in the queue are playing vs. pending
          cmd = '%s.primary_queue' % (q)
          response = parse_command(host, host_settings, cmd)
          if response is not None:
            offset = len(response.split(' '))
          else:
            offset = 0
          request_list[q]['offset'] = offset

          # Finally grab all the rids in the request queue (no matter the type)
          request_list[q]['rids'] = parse_rid_list(host, host_settings, "%s.queue" % (q))
	if request_list == []:
		return None
        #assert False
	return request_list;
	
def build_status_list(host, host_settings, streams, available_commands):
	status = {}
	status['host'] = str(host)
	status['ip_address'] = str(host.ip_address)
	status['base_url'] = str(host.base_url)
	command_list = ['version', 'uptime']
	for name in streams:
		command_list.append(name+".status")
		command_list.append(name+".remaining")
	for command in command_list:
		if command in available_commands:
			response = parse_command(host, host_settings, command)
			response = response.splitlines()
			if(len(response) > 0):
				response = response[0]
				status[command] = response
	return status

def get_host_list():
	h = Host.objects.all()
	return h   
def get_air_queue(host, host_settings):
  queue = {}
  v = Version.objects.get(host__version__exact=host.version)
  if v.version == '0.9.x':
    on_air = 'on_air'
  else:
    on_air = 'request.on_air'
  queue['on_air'] = {}
  queue['on_air']['rids'] = parse_rid_list(host, host_settings, on_air)
  return queue

def get_alive_queue(host, host_settings):
  queue = {}
  v = Version.objects.get(host__version__exact=host.version)
  if v.version == '0.9.x':
    alive = 'alive'
  else:
    alive = 'request.alive'
  queue['alive'] = {}
  queue['alive']['rids'] = parse_rid_list(host, host_settings, alive)
  return queue

############################################################################
#	Begin Main 'Display' Functions
#	Functions that display main pages with full layouts
############################################################################

def index (request):
	host_list = get_host_list()
	quickstatus = {}
	#loop through hosts and grab status for each one
	for host in host_list:
		host_settings = Setting.objects.filter(hostname__exact=host)
		template_dict = {}
		host_online = is_online(host, host_settings)
		if host_online:
			#Parse all available help commands (for reference)	
			help = parse_help(host, host_settings)
			
			#Get active nodes for this host and this liquidsoap instance
			node_list = parse_node_list(host, host_settings)
			out_streams = parse_output_streams(host, host_settings, node_list)
			out_streams = sorted(out_streams)
			status = build_status_list(host, host_settings, out_streams, help)
			
			#Instantiate a dictionary for Metadata, RIDs will reference this dictionary.
			metadata_storage = {}
		
			#Get 'on_air' Queue and Grab Metadata for it
			air_queue = get_air_queue(host, host_settings)
			metadata_storage = parse_queue_metadata(host, host_settings, air_queue, metadata_storage)
			
			#Get 'alive' Queue and Grab Metadata for it
			alive_queue = get_alive_queue(host, host_settings)
			metadata_storage = parse_queue_metadata(host, host_settings, alive_queue, metadata_storage)
				
			template_dict['online'] = host_online
			template_dict['node_list'] = node_list
			template_dict['out_streams'] = out_streams
			template_dict['status'] = status
			template_dict['air_queue'] = air_queue
			template_dict['alive_queue'] = alive_queue
			template_dict['metadata_storage'] = metadata_storage
		else:
			template_dict['online'] = host_online
		
		quickstatus[host]=template_dict
	return render_to_response('index.html', {'hosts': host_list, 'quickstatus': quickstatus}, context_instance=RequestContext(request))

@login_required	
def display_status(request, host_name):
	logging.info('Start of display_status()')
	if request.method == 'GET':		
		host = get_object_or_404(Host, name=host_name)
		host_settings = get_list_or_404(Setting, hostname=host)
		t = Theme.objects.get(host__name__exact=host_name)
		template_dict = {}
		try:
			pg_num = request.GET['pg']
		except:
			pg_num=1
		try:
			# If there is a search string parameter,
			# set search to active and pass along the
			# the query string so ajax calls know what to search
			search = request.GET['search']
			template_dict['search'] = True
			template_dict['query_string'] = request.META['QUERY_STRING']
		except:
			template_dict['search'] = False
		
		template_dict['pool_page'] = pg_num
		template_dict['active_host'] = host
		template_dict['hosts'] = get_host_list()
		template_dict['theme'] = t.name
		logging.info('End of display_status() with GET')
		return render_to_response('controller/status.html', template_dict, context_instance=RequestContext(request))
	else:
		logging.info('End of display_status() with POST')
		return

def display_error(request, host_name, template, msg):		
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	t = Theme.objects.get(host__name__exact=host_name)
	pg_num=1
	template_dict = {}
	template_dict['error'] = msg
	template_dict['search'] = False
	template_dict['pool_page'] = pg_num
	template_dict['active_host'] = host
	template_dict['hosts'] = get_host_list()
	template_dict['theme'] = t.name
	return render_to_response(template, template_dict, context_instance=RequestContext(request))

def display_alert(request, host_name, template, msg):		
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	t = Theme.objects.get(host__name__exact=host_name)
	pg_num=1
	template_dict = {}
	template_dict['alert'] = msg
	template_dict['search'] = False
	template_dict['pool_page'] = pg_num
	template_dict['active_host'] = host
	template_dict['hosts'] = get_host_list()
	template_dict['theme'] = t.name
	return render_to_response(template, template_dict, context_instance=RequestContext(request))

############################################################################
#	Begin Asynchronous 'Display' Functions
#	Functions that display discrete data
#	Minimal table views created for individual tabs
#	All are called directly by urls.py
############################################################################	
	
@login_required	
def display_nodes(request, host_name):
  logging.info('Start of display_nodes()')
  host = get_object_or_404(Host, name=host_name)
  host_settings = get_list_or_404(Setting, hostname=host)

  #Parse all available help commands (for reference)	
  help = parse_help(host, host_settings)

  #Get active nodes for this host and this liquidsoap instance
  node_list = parse_node_list(host, host_settings)
  out_streams = parse_output_streams(host, host_settings, node_list)
  out_streams = sorted(out_streams)
  in_streams = parse_input_streams(host, host_settings, node_list)
  in_streams = sorted(in_streams)
  status = build_status_list(host, host_settings, out_streams, help)

  # Get list of interactive variables for each host
  var_list = parse_var_list(host, host_settings)

  #Instantiate a dictionary for Metadata, RIDs will reference this dictionary.
  metadata_storage = {}

  #Get 'on_air' Queue and Grab Metadata for it
  air_queue = get_air_queue(host, host_settings)
  metadata_storage = parse_queue_metadata(host, host_settings, air_queue, metadata_storage)

  #Get 'alive' Queue and Grab Metadata for it
  alive_queue = get_alive_queue(host, host_settings) 
  metadata_storage = parse_queue_metadata(host, host_settings, alive_queue, metadata_storage)

  template_dict = {}
  template_dict['active_host'] = host
  template_dict['node_list'] = node_list
  template_dict['out_streams'] = out_streams
  template_dict['in_streams'] = in_streams
  template_dict['var_list'] = var_list
  template_dict['status'] = status
  template_dict['air_queue'] = air_queue
  template_dict['alive_queue'] = alive_queue
  template_dict['metadata_storage'] = metadata_storage

  logging.info('End of display_nodes()')
  return render_to_response('controller/nodes.html', template_dict, context_instance=RequestContext(request))

@login_required	
def display_queues(request, host_name):
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	#Instantiate a dictionary for Metadata, RIDs will reference this dictionary.
	template_dict = {}
	metadata_storage = {}
	
	#Get 'request' Queues and Grab Metadata for them
	queue = parse_queue_dict(host, host_settings)
	template_dict['metadata_storage'] = parse_queue_metadata(host, host_settings, queue, metadata_storage)
	template_dict['queue'] = queue
	return render_to_response('controller/queues.html', template_dict, context_instance=RequestContext(request))
	
def display_history(request, host_name):
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	
	#Get active nodes for this host and this liquidsoap instance
	node_list = parse_node_list(host, host_settings)
	#Instantiate a dictionary for Metadata, RIDs will reference this dictionary.
	template_dict = {}
	metadata_storage = {}
	
	#Get 'history' Listing and Grab Metadata for it.
	history = parse_history(host, host_settings, node_list)
	template_dict['active_host'] = host
	template_dict['metadata_storage'] = parse_queue_metadata(host, host_settings, history, metadata_storage)
	template_dict['history'] = history
	
	if request.method == 'GET':
		try:
			 format = request.GET['format']
			 if (format == 'rss'):
			 	template_file = 'history.rss'
			 	mime_output = 'application/rss+xml'
		except:
			template_file = 'history.html'
			mime_output = 'text/html'
	else:
		 template_file = 'history.html'
		 mime_output = 'text/html'
	return render_to_response('controller/'+template_file, template_dict, context_instance=RequestContext(request), mimetype=mime_output)

@login_required	
def display_help(request, host_name):
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	
	#Instantiate a dictionary for Metadata, RIDs will reference this dictionary.
	template_dict = {}
	
	#Parse all available help commands (for reference)	
	template_dict['help'] = parse_help(host, host_settings)
	return render_to_response('controller/help.html', template_dict, context_instance=RequestContext(request))

@login_required	
def display_pool_page(request, host_name, type, page):
	logging.info('Start of display_pool_page()')
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, host_settings)
	template_dict = {}
	p = get_song_pager()
	try:
		single_page = p.page(page)
	except EmptyPage, InvalidPage:
		single_page = p.page(p.num_pages)
	template_dict['all_pages'] = p
	template_dict['single_page'] = single_page
	template_dict['active_host'] = host
	template_dict['node_list'] = node_list
	logging.info('End of display_pool_page()')
	return render_to_response('controller/pool.html', template_dict, context_instance=RequestContext(request))

@login_required
def display_pool(request, host_name, type):
	host = get_object_or_404(Host, name=host_name)
	template_dict = {}
	#populate both dictionaries to avoid template errors.
	all_pages = get_song_pager()
	template_dict['all_pages'] = all_pages
	template_dict['single_page'] = all_pages
	template_dict['active_host'] = host
	return render_to_response('controller/pool.html', template_dict, context_instance=RequestContext(request))

@login_required
def search_pool(request, host_name, page):
  logging.info('Start of search_pool()')
  if request.method == 'GET':
    host = get_object_or_404(Host, name=host_name)
    host_settings = get_list_or_404(Setting, hostname=host)
    node_list = parse_node_list(host, host_settings)
    template_dict = {}
		
    # Start the search process
    try:
      cat = request.GET['type']
    except:
      cat = 'song'

    try:
      term = request.GET['search']
      results = Song.objects.filter(title__icontains=term).order_by('album__name', 'track')
      results = results | Song.objects.filter(artist__name__icontains=term).order_by('album__name', 'track')
      results = results | Song.objects.filter(album__name__icontains=term).order_by('album__name', 'track')
      results = results | Song.objects.filter(genre__name__icontains=term).order_by('album__name', 'track')
    except:
      term = ''
      results = Song.objects.all()

    #populate the paginator using the search queryset.		
    p = get_song_search_pager(results)
    try:
      single_page = p.page(page)
    except EmptyPage, InvalidPage:
      single_page = p.page(p.num_pages)
    
    #place all the information we gathered into the template dictionary
    template_dict['node_list'] = node_list
    template_dict['active_host'] = host
    template_dict['search'] = True
    template_dict['search_term'] = term
    template_dict['all_pages'] = p
    template_dict['single_page'] = single_page
    template_dict['pool_page'] = page
    logging.info('End of search_pool_page() with GET')
    return render_to_response('controller/pool_search.html', template_dict, context_instance=RequestContext(request))
  else:
    #return message about Post with bad parameters.
    message = 'Search cannot be executed via POST requests.'
    logging.info('End of search_pool_page() with POST')
    return display_error(request, host_name, 'controller/pool.html', message)

############################################################################
#	Begin 'Action' Functions
#	Functions act on liquidsoap servers 
#	START, STOP, PUSH, ETC...
#	All are called directly by urls.py
############################################################################
	
@login_required
def stream_skip(request, host_name, stream):
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, host_settings)
	if(stream in node_list):
		response = parse_command(host, host_settings, '%s.skip' % (str(stream)))
		response = response.splitlines()
		if('Done' in response):
			#time.sleep(0.75)
			return HttpResponseRedirect('/'+settings.BASE_URL+'status/'+host_name)
		else:
			return HttpResponse(status=404)
	else:
		raise Http404

@login_required
def stream_stop(request, host_name, stream):
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, host_settings)
	if(stream in node_list):
		response = parse_command(host, host_settings, '%s.stop' % (str(stream)))
		response = response.splitlines()
		if '' in response:
			time.sleep(0.2)
			return HttpResponseRedirect('/'+settings.BASE_URL+'status/'+host_name)
		else:
			return HttpResponse(status=500)
	else:
		raise Http404

@login_required
def stream_start(request, host_name, stream):
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, host_settings)
	if(stream in node_list):
		response = parse_command(host, host_settings, '%s.start' % (str(stream)))
		response = response.splitlines()
		if('' in response):
			time.sleep(0.2)
			return HttpResponseRedirect('/'+settings.BASE_URL+'status/'+host_name)
		else:
			return HttpResponse(status=500)
	else:
		raise Http404

@login_required
def set_variable(request, host_name):
  message = ''
  if request.method == 'GET':
    scope = request.GET['scope']
    var = request.GET['variable']
    value = request.GET['value']
    host = get_object_or_404(Host, name=host_name)
    host_settings = get_list_or_404(Setting, hostname=host)
    var_list = parse_var_list(host, host_settings)
    if scope in var_list and var in var_list[scope]:
      # XXX: we need a proper way to test validity of new values
      # For now, this is what we do
      # There are two types of liquidoap interactive vars: float and string
      if var_list[scope][var]['type'] == 'float':
        value = float(value)
      else:
        value = str(value)
      response = parse_command(host, host_settings, "var.set %s_%s = %s" % (scope, var, value))
      if (response is not None): # and (re.search("Variable \w+ set", response)):
        # success
        return HttpResponse("OK")
      else:
        message = "there was a problem setting the new value"
    else:
      message = "scope or variable not defined" 
  else:
    #return message about Get with bad parameters.
    message = 'Volume cannot be adjusted via GET requests.'
  return display_error(request, host_name, 'controller/status.html', message)

@login_required
def queue_push(request, host_name):
  ajax = {}
  if request.method == 'POST':
    if (request.POST['song_uri']):
      uri_id = request.POST['song_uri']
      s = get_object_or_404(Song, pk=uri_id)
    elif (request.POST['album_uri']):
      uri_id = request.POST['album_uri']
      s = get_list_or_404(Song, album__exact=uri_id)

    #if the uri exists, then process the request
    host = get_object_or_404(Host, name=host_name)
    host_settings = get_list_or_404(Setting, hostname=host)

    #Parse all available help commands (for reference)
    help = parse_help(host, host_settings)

    #Make sure that the queue we have is valid.
    #Check Database and liquidsoap instance
    queue_name = request.POST['queue']
    get_object_or_404(Setting, data=queue_name)
    queue_command = queue_name+'.push'
    check_command = smart_str(queue_command+' <uri>')
    if check_command in help:
      #we are okay to continue processing the request
      queue_command += ' '+s.filename
      queue_command = smart_str(queue_command)
    else:
      raise Http404

    #commit the command
    logging.info('Pushing to queue: %s' % queue_command)
    response = parse_command(host, host_settings, queue_command)
    logging.info('Response is: %s' % response)
    if (True): #(re.search('^\d+$', response)):
      ajax['type'] = 'info'
      ajax['msg'] = 'new rid %s' % response
    else:
      ajax['type'] = 'error'
      ajax['msg'] = 'something went wrong'
  else:
    #return message about Get with bad parameters.
    ajax['type'] = 'error'
    ajax['msg'] = 'Requests cannot be pushed via GET requests.'
  return HttpResponse(simplejson.dumps(ajax), mimetype='application/json')

def queue_reorder(request, host_name):
  if request.method == 'GET':
    ajax = {};
    # Make sure the queue accepts a move
    host = get_object_or_404(Host, name=host_name)
    host_settings = get_list_or_404(Setting, hostname=host)
    help_list = parse_help(host, host_settings)

    queue_name = request.GET['queue']
    queue_op = queue_name + '.move'
    queue_op_help = queue_op + ' <rid> <pos>'
    if ( queue_op_help not in help_list ):
      message = 'Queue Operation not valid: %s help_list: %s' % (queue_op, help_list)
      #return display_error(request, host_name, 'controller/status.html', message)
      return HttpResponse(message)

    # Check to make sure the rid exists and is not playing
    rid = request.GET['rid']
    on_air = parse_rid_list(host, host_settings, 'on_air')
    queue_list  = parse_queue_dict(host, host_settings)
    if (rid not in queue_list[queue_name]['rids']) or (rid in on_air):
      ajax['type'] = 'error'
      ajax['msg'] = 'RID is not valid or cannot be moved: %s\nqueue: %s\non_air: %s' % (rid, queue_list[queue_name]['rids'], on_air)
    else:
      # Attempt the rid move
      position = request.GET['pos']
      command = '%s %s %s' % (queue_op, rid, position)
      response = parse_command(host, host_settings, command)

      # Return an OK or something similar to the ajax call
      if (response == 'OK'):
        # success
        ajax['type'] = 'info';
      else:
        ajax['type'] = 'error';
      ajax['msg'] = response;
  else:
    #return message about Get with bad parameters.
    ajax['type'] = 'info'
    ajax['msg'] = 'Requests cannot be moved via GET requests.'
  return HttpResponse(simplejson.dumps(ajax), mimetype='application/json')

def commit_log(host_name):
	# sleep a certain amount of time 
	# to allow 'on_air' metadata to register 
	# the possibility of a new track.
	time.sleep(0.5)
	
	host = get_object_or_404(Host, name=host_name)
	host_settings = get_list_or_404(Setting, hostname=host)	#Get active nodes for this host and this liquidsoap instance
	
	node_list = parse_node_list(host, host_settings)
	#Instantiate a dictionary for Metadata, RIDs will reference this dictionary.
	history = {}
	metadata_storage = {}

	#Get 'on_air' Queue and Grab Metadata for it
	air_queue = get_air_queue(host, host_settings)
	metadata_storage = parse_queue_metadata(host, host_settings, air_queue, metadata_storage)
	
	#Get 'history' and Grab Metadata for it
	history = parse_history(host, host_settings, node_list)
	metadata_storage = parse_queue_metadata(host, host_settings, history, metadata_storage)
			
	for name, entries in history.iteritems():
		name = replacedot(name)
		for i, e in enumerate(reversed(entries)): #reverse for descending order
			if i == 0: #only write log entry for the latest on_air entry							
				for rid, listing in metadata_storage.iteritems():
					if e == rid:
						#this is the 'latest' on_air entry and 
						#it matches a metadata listing
						try:
							log = Log.objects.get(Q(entrytime__exact=listing['on_air']),
												  Q(stream__exact=name))
						except Log.DoesNotExist:
							try:
								results = Song.objects.filter(Q(title__iexact=listing['title']),
								  Q(artist__name__iexact=listing['artist']),
								  Q(album__name__iexact=listing['album']),
								  Q(genre__name__iexact=listing['genre'])).distinct()[0]
								id = results.id
							except(IndexError):
								id = -1
							log = Log(
						    	entrytime = listing['on_air'],
						    	info = 'RADIO_HISTORY',
						    	host = host,
						    	stream = name,
						    	song_id = id,
						    	title = listing['title'],
						    	artist = listing['artist'],
						    	album = listing['album'],
								)
							log.save()
	
def write_log(request, host_name):
	if request.method == 'GET':		
		t = Thread(target=commit_log, args=[host_name])
		t.setDaemon(True)
		t.start()
		return render_to_response('controller/log.html', {}, context_instance=RequestContext(request))
	else:
		return HttpResponse(status=500)

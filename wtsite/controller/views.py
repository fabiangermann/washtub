from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.template import RequestContext
from django.conf import settings
from wtsite.controller.models import *

import telnetlib, string

# Create your views here.
def parse_command(host, settings, command):
	port = None
	for p in settings:
	   if p.value == 'port':
	       port = str(p.data)
	#default port number (for telnet)
	if not port:
		port = '1234' 
	command+='\n'
	tn = telnetlib.Telnet(str(host.ip_address), port)
	tn.write(command)
	response = tn.read_until("END")
	tn.close()
	return response

def parse_metadata(host, settings, rid):
	meta_list = parse_command(host, settings, 'metadata %s\n' % rid)
	meta_list = meta_list.splitlines()
	metadata = {}
	for m in meta_list:
		m = m.split('=')
		if m[0] != 'END':
			metadata[m[0]] = m[1].strip('"')
	return metadata

def parse_queue_metadata(host, settings, queue, storage):
	if not storage:
	   storage = {}
	if queue:
		for name,entries in queue.iteritems():
			for rid in entries:
				if rid not in storage:
					storage[rid]= parse_metadata(host, settings, rid)
	return storage

def parse_node_list(host, settings):
	list = parse_command(host, settings, "list")
	list = list.splitlines()
	out = {}
	for item in list:
		if item != 'END':
			item = item.split(' : ')
			out[item[0]]=item[1]
	return out

def parse_help(host, settings):
	list = parse_command(host, settings, "help")
	list = list.splitlines()
	out = []
	for item in list:
		if item.startswith('|'):
			item = item.lstrip('| ')
			out.append(item)
	list = out
	return list

def parse_rid_list(host, settings, command):
	entry = parse_command(host, settings, command)
	entry = entry.split()
	entry_list = []
	for e in entry:
		if e != 'END':
		 entry_list.append(e)
	return entry_list

def parse_output_streams(host, settings, node_list):
	streams = []
	for node,type in node_list.iteritems():
		temp = type.split('.')
		if ('output' in temp):
			streams.append(node)
	return streams
							
def parse_history(host, settings, node_list):
	history = {}
	for node,type in node_list.iteritems():
		type = type.split('.')
		if (len(type) > 0):
			if ('output' in type):
				entry_list = []
				output = parse_command(host, settings, '%s.metadata\n' % (node))
				output = output.splitlines()
				for line in output:
					line = line.split('=')
					if( 'rid' in line):
						if ( len(line) > 1 ):
							entry_list.append(line[1].strip('"'))
				found = False
				for name,list in history.iteritems():
					if(list == entry_list):
					   found = True
					   new_name = name+', '+node
					   history[new_name] = entry_list
					   del history[name]
				if(not found):
					node = node
					history[node] = entry_list
	return history

def parse_queue_dict(host, settings):
	queue_list = []
	for p in settings:
	   if p.value == 'queue_id':
	   	queue_list.append(str(p.data))
	#default port number (for telnet)
	if queue_list == []:
		return None
	request_list = {}
	for q in queue_list:
		request_list[q] = parse_rid_list(host, settings, "%s.queue" % (q))
	if request_list == []:
		return None
	return request_list;
	
def build_status_list(host, settings, streams, available_commands):
	status = {}
	status['host'] = str(host)
	status['ip address'] = str(host.ip_address)
	command_list = ['version', 'uptime']
	for name in streams:
		command_list.append(name+".status")
		command_list.append(name+".remaining")
	for command in command_list:
		if command in available_commands:
			response = parse_command(host, settings, command)
			response = response.splitlines()
			if(len(response) > 0):
				response = response[0]
				status[command] = response
	return status

def get_host_list():
	h = Host.objects.all()
	return h   

@login_required()
def display_status(request, host_name):
	host = get_object_or_404(Host, name=host_name)
	settings = get_list_or_404(Setting, hostname=host)	
	help = parse_help(host, settings)
	node_list = parse_node_list(host, settings)
	streams = parse_output_streams(host, settings, node_list)
	streams = sorted(streams)
	status = build_status_list(host, settings, streams, help)
	
	metadata_storage = {}
	history = parse_history(host, settings, node_list)
	metadata_storage = parse_queue_metadata(host, settings, history, metadata_storage)

	#Get Request Queue and Grab Metadata for it
	queue = parse_queue_dict(host, settings)
	metadata_storage = parse_queue_metadata(host, settings, queue, metadata_storage)
	
	#Get 'on_air' Queue and Grab Metadata for it
	air_queue = {}
	air_queue['on_air'] = parse_rid_list(host, settings, "on_air")
	metadata_storage = parse_queue_metadata(host, settings, air_queue, metadata_storage)
	
	#Get 'alive' Queue and Grab Metadata for it
	alive_queue = {}
	alive_queue['alive'] = parse_rid_list(host, settings, "alive")
	metadata_storage = parse_queue_metadata(host, settings, alive_queue, metadata_storage)
	
	hosts = get_host_list()
	active_host = host
	return render_to_response('controller/status.html', {'metadata_storage': metadata_storage,
														 'history': history,
														 'streams': streams,
														 'alive_queue': alive_queue,
														 'air_queue': air_queue, 
														 'queue': queue, 
														 'active_host': active_host, 
														 'hosts': hosts, 
														 'help': help, 
														 'node_list': node_list,
														 'status': status
														 }, context_instance=RequestContext(request))

def index (request):
	hosts = get_host_list()
	return render_to_response('index.html', {'hosts': hosts}, context_instance=RequestContext(request))

@login_required
def stream_skip(request, host_name, stream):
	host = get_object_or_404(Host, name=host_name)
	settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, settings)
	if(stream in node_list):
		response = parse_command(host, settings, '%s.skip\n' % (str(stream)))
		response = response.splitlines()
		if('Done' in response):
			return HttpResponseRedirect('/washtub/control/'+host_name)
		else:
			return HttpResponse(status=404)

@login_required
def stream_stop(request, host_name, stream):
	host = get_object_or_404(Host, name=host_name)
	settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, settings)
	if(stream in node_list):
		response = parse_command(host, settings, '%s.stop\n' % (str(stream)))
		response = response.splitlines()
		if('' in response):
			return HttpResponseRedirect('/washtub/control/'+host_name)
		else:
			return HttpResponse(status=500)
	raise Http404

@login_required
def stream_start(request, host_name, stream):
	host = get_object_or_404(Host, name=host_name)
	settings = get_list_or_404(Setting, hostname=host)
	node_list = parse_node_list(host, settings)
	if(stream in node_list):
		response = parse_command(host, settings, '%s.start\n' % (str(stream)))
		response = response.splitlines()
		if('' in response):
			return HttpResponseRedirect('/washtub/control/'+host_name)
		else:
			HttpResponse(status=500)
	raise Http404
	
	
	
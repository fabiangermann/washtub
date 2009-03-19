from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from wtsite.controller.models import *
from django.conf import settings
import telnetlib, string

# Create your views here.
def parse_command(host, settings, command):
	command+='\n'
	tn = telnetlib.Telnet(host, settings.port)
	tn.write(command)
	response = tn.read_until("END")
	tn.close()
	response = response.splitlines()
	response = response[0]
	return response

def parse_help(host, settings):
	tn = telnetlib.Telnet(host, settings[0])
	tn.write("help\n")
	help = tn.read_until("END")
	tn.close()
	list = help.splitlines()
	out = []
	for item in list:
		if item.startswith('|'):
			item = item.lstrip('| ')
			out.append(item)
	list = out
	return list

def build_status_list(host, settings, available_commands):
	status = []
	command_list = ['on_air', 'alive', 'version', 'uptime']
	for command in command_list:
		if command in available_commands:
			response = parse_command(host, settings, command)
			response = [command, response]
			status.append(response)
	return status

def get_host_list():
	h = Host.objects.all()
	return h   

@login_required()
def display_status(request, host_name):
	h = get_object_or_404(Host, name=host_name)
	try:
		settings = h.setting_set.all()	
	except Setting.DoesNotExist:
		raise Http404
	help = parse_help(h, settings)
	status = build_status_list(h, settings, help)
	hosts = get_host_list()
	return render_to_response('controller/status.html', {'hosts': hosts, 'help': help, 'status': status}, context_instance=RequestContext(request))

def index (request):
	hosts = get_host_list()
	return render_to_response('index.html', {'hosts': hosts}, context_instance=RequestContext(request))


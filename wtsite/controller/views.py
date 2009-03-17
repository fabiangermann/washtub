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
def parse_help(input):
	list = input.splitlines()
	out = []
	for item in list:
		if item.startswith('|'):
			item = item.lstrip('|')
			out.append(item)
	list = out
	return list

def get_host_list():
	h = Host.objects.all()
	return h   

@login_required()
def display_status(request):
	tn = telnetlib.Telnet("localhost", 1234)
	tn.write("help\n")
	status = tn.read_until("END")
	tn.close()
	status = parse_help(status)
	hosts = get_host_list()
	return render_to_response('controller/status.html', {'hosts': hosts}, {'status': status}, context_instance=RequestContext(request))

def index (request):
	hosts = get_host_list()
	return render_to_response('index.html', {'hosts': hosts}, context_instance=RequestContext(request))


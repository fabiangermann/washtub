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
	list = input.splitline()
	out = []
	for item in list:
		if item.startswith('|'):
			item.lstrip('|')
			out.append(item)
	list = out
	return list

@login_required()
def display_status(request):
	tn = telnetlib.Telnet("localhost", 1234)
	tn.write("help\n")
	status = tn.read_until("END")
	tn.close()
	status = parse_help(status)
	return render_to_response('controller/status.html', {'status': status}, context_instance=RequestContext(request))


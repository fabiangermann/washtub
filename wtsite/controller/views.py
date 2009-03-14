from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from wtsite.controller.models import *
from django.conf import settings

# Create your views here.
@login_required()
def display_status(request):
	status = "test"
	return render_to_response('controller/status.html', {'status': status}, context_instance=RequestContext(request))


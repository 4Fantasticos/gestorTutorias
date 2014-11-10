from django.shortcuts import render_to_response
from django.template import RequestContext
from tutorias.models import *

def alumnos(request):
    p = User.objects.all()
    return render_to_response('index.html',{'alumnos':p})
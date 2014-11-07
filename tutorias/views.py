from django.shortcuts import render_to_response
from django.template import RequestContext
from tutorias.models import Alumno
from tutorias.form import AlumnoForm

def alumnos(request):
    p = Alumno.objects.all()
    return render_to_response('index.html',{'alumnos':p})

def formularioAlumnos(request):
    form = AlumnoForm()
    return render_to_response('crearAlumnos.html',{'form':form},context_instance=RequestContext(request))


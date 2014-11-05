from django.shortcuts import render
from django.http import HttpResponse
from tutorias.models import Alumno
def index(request):
    p = Alumno.objects.get(pk=2)
    return HttpResponse(p.nombre)

def laura(request):
    return HttpResponse("Laura putilla!!!")

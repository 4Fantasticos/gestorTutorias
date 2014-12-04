# encoding:utf-8
__author__ = 'Fran'
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from tutorias.models import *
from tutorias.form import *
import datetime

def miPanel(request):
    context = RequestContext(request)
    if request.user.is_superuser:
        usuarios = User.objects.exclude(username='admin')
        grados =Grado.objects.all()
        asignaturas = Asignatura.objects.all()
        datos = {'usuarios': len(usuarios), 'grados': len(grados), 'asignaturas': len(asignaturas)}
        return render_to_response('miPanel.html', {'datos': datos}, context)
    elif request.user.es_profesor:
        reservas =Reserva.objects.filter(horario__profesor=request.user, estado='P')
        datos = {'reservas': len(reservas)}
        return render_to_response('miPanel.html', {'datos': datos},context)
    else:
        return render_to_response('miPanel.html', {},context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def addAsignaturasAlumnos(request):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=request.session['alumno'])
    grado = get_object_or_404(Grado, identificador=request.session['grado'])
    asignaturas = Asignatura.objects.filter(grados=grado)
    if request.method == 'POST':
        form = AddAsignaturasForm(request.POST, asignaturas=asignaturas)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                asig = Asignatura.objects.get(id=item)
                asig.usuarios.add(user)
            return HttpResponseRedirect(reverse('miPanel'))
        else:
            form = AddAsignaturasForm(request.POST, asignaturas=asignaturas)
            return render_to_response('formAddAsignaturas.html', {'form': form, 'asignaturas': asignaturas}, context)
    form = AddAsignaturasForm(asignaturas=asignaturas)
    return render_to_response('formAddAsignaturas.html', {'form': form, 'asignaturas': asignaturas}, context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def addGradosProfesor(request):
    context =RequestContext(request)
    user =get_object_or_404(User,pk=request.session['profesor'])
    grados =Grado.objects.all()
    if request.method =='POST':
        form = AddGradosForm(request.POST,grados=grados)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                grado = Grado.objects.get(id=item)
                grado.profesores.add(user)
        request.session['profesor'] = user.id
        return HttpResponseRedirect(reverse('add_asignaturas_profesor'))
    else:
        form = AddGradosForm(request.POST, grados=grados)
        return render_to_response('formAddGrados.html', {'form': form, 'grados': grados}, context)
    form = AddGradosForm(grados=grados)
    return render_to_response('formAddGrados.html', {'form': form, 'grados': grados}, context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def addAsignaturasProfesor(request):
    context =RequestContext(request)
    user =get_object_or_404(User, pk=request.session['profesor'])
    listaAsignaturas = []
    grados =Grado.objects.filter(profesores=user)
    for grado in grados:
        asignaturas =Asignatura.objects.filter(grados=grado)
        for asignatura in asignaturas:
            listaAsignaturas.append(asignatura)
    if request.method == 'POST':
        form = AddAsignaturasForm(request.POST,asignaturas=asignaturas)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                asig = Asignatura.objects.get(id=item)
                asig.profesores.add(user)
            return HttpResponseRedirect(reverse('miPanel'))
        else:
            form = AddAsignaturasForm(request.POST,asignaturas=asignaturas)
            return render_to_response('formAddAsignaturas.html',
                                      {'profesor': True, 'form': form, 'asignaturas': asignaturas}, context)
    form = AddAsignaturasForm(asignaturas=asignaturas)
    return render_to_response('formAddAsignaturas.html', {'profesor': True, 'form': form, 'asignaturas': asignaturas},
                              context)





@user_passes_test(lambda u: u.es_profesor, login_url='/')
def notificacionesProfesor(request):
    context = RequestContext(request)
    if 'aceptar' in request.POST:
        id = request.POST.get('id')
        reserva = Reserva.objects.get(id=id)
        reserva.estado = 'R'
        reserva.save()
    elif 'declinar' in request.POST:
        id = request.POST.get('id')
        textoProfesor = request.POST.get('texto')
        reserva = Reserva.objects.get(id=id)
        reserva.mensajeCancel = textoProfesor
        reserva.estado = 'C'
        reserva.save()
    notificaciones = Reserva.objects.filter(horario__profesor=request.user).filter(estado='P')
    reservas = Reserva.objects.filter(horario__profesor=request.user).filter(estado='R').filter(dia__gt=datetime.datetime.now)
    aceptadas_lista = Reserva.objects.filter(horario__profesor=request.user).filter(estado='R').filter(dia__lt=datetime.datetime.now)
    paginator_aceptadas = Paginator(aceptadas_lista, 10)
    page_aceptadas = request.GET.get('page_a')
    try:
        aceptadas = paginator_aceptadas.page(page_aceptadas)
    except PageNotAnInteger:
        aceptadas = paginator_aceptadas.page(1)
    except EmptyPage:
        aceptadas = paginator_aceptadas.page(paginator_aceptadas.num_pages)
    canceladas_lista = Reserva.objects.filter(horario__profesor=request.user).filter(estado='C')
    paginator_canceladas = Paginator(canceladas_lista, 10)
    page_canceladas = request.GET.get('page_c')
    try:
        canceladas = paginator_canceladas.page(page_canceladas)
    except PageNotAnInteger:
        canceladas = paginator_canceladas.page(1)
    except EmptyPage:
        canceladas = paginator_canceladas.page(paginator_canceladas.num_pages)
    return render_to_response('misNotificaciones.html',{'notificaciones': notificaciones, 'reservas': reservas, 'canceladas': canceladas,'aceptadas': aceptadas},context)

@user_passes_test(lambda u: not u.es_profesor, login_url='/')
def notificacionesAlumno(request):
    context = RequestContext(request)
    notificaciones = Reserva.objects.filter(alumnos=request.user).filter(estado='P')
    reservas = Reserva.objects.filter(alumnos=request.user).filter(estado='R').filter(
        dia__gt=datetime.datetime.now)
    aceptadas_lista = Reserva.objects.filter(alumnos=request.user).filter(estado='R').filter(
        dia__lt=datetime.datetime.now)
    paginator_aceptadas = Paginator(aceptadas_lista, 10)
    page_aceptadas = request.GET.get('page_a')
    try:
        aceptadas = paginator_aceptadas.page(page_aceptadas)
    except PageNotAnInteger:
        aceptadas = paginator_aceptadas.page(1)
    except EmptyPage:
        aceptadas = paginator_aceptadas.page(paginator_aceptadas.num_pages)
    canceladas_lista = Reserva.objects.filter(alumnos=request.user).filter(estado='C')
    paginator_canceladas = Paginator(canceladas_lista, 10)
    page_canceladas = request.GET.get('page_c')
    try:
        canceladas = paginator_canceladas.page(page_canceladas)
    except PageNotAnInteger:
        canceladas = paginator_canceladas.page(1)
    except EmptyPage:
        canceladas = paginator_canceladas.page(paginator_canceladas.num_pages)
    return render_to_response('misNotificacionesAlumnos.html',
                              {'notificaciones': notificaciones, 'reservas': reservas, 'canceladas': canceladas,'aceptadas': aceptadas},context)

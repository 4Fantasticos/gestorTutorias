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

@user_passes_test(lambda u: u.es_profesor, login_url='/')
def add_horario(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = HorarioForm(request.POST)

        if form.is_valid():
            user =request.user
            dia_semana =form.cleaned_data['dia_semana']
            hora_inicio =form.cleaned_data['hora_inicio']
            hora_final =form.cleaned_data['hora_final']
            date_inicio =datetime.datetime.combine(datetime.date.today(), hora_inicio)
            date_fin =datetime.datetime.combine(datetime.date.today(), hora_final)
            diff = date_fin - date_inicio
            minutos = diff.total_seconds() / 60
            intervalos = minutos // 15
            mas15 =datetime.timedelta(0, 900)
            horarios_en_bd = Horario.objects.filter(profesor=user).filter(dia_semana=dia_semana)
            for i in range(int(intervalos)):
                horario =Horario(dia_semana=dia_semana, hora_inicio=date_inicio.time(), profesor=user)
                horarios_en_bd = list(Horario.objects.filter(profesor=user).filter(dia_semana=dia_semana).filter(hora_inicio=date_inicio.time))
                print ('#######DEBUG######')
                print horarios_en_bd
                if horarios_en_bd == []:
                    horario.save()
                date_inicio = date_inicio + mas15

            return HttpResponseRedirect(reverse('miPanel'))
        else:
            return render_to_response('formularioHorario.html', {'form': form}, context)

    form = HorarioForm()
    return render_to_response('formularioHorario.html', {'form': form, 'dias': DIAS_DE_LA_SEMANA}, context)

@user_passes_test(lambda u: u.es_profesor, login_url='/')
def eliminar_horario(request, horario_id):
    horario = Horario.objects.filter(profesor=request.user).filter(pk=horario_id)
    horario.delete()
    return HttpResponseRedirect(reverse('misHorarios'))

@user_passes_test(lambda u: u.es_profesor, login_url='/')
def mis_horarios(request):
    context =RequestContext(request)
    user =request.user
    horarios =Horario.objects.filter(profesor=user)
    return render_to_response('misHorarios.html', {'horarios': horarios},context)

@user_passes_test(lambda u: not u.es_profesor, login_url='/')
def horarios_profesores(request, profesor_id):
    context = RequestContext(request)
    horarios = Horario.objects.filter(profesor=profesor_id)
    lista_dias = []
    hoy = datetime.datetime.now()
    mas1dia = datetime.timedelta(1, 0)
    dossemanas = hoy + datetime.timedelta(14, 0)
    lunes, martes, miercoles, jueves, viernes = -1, -1, -1, -1, -1
    for h in horarios:
        if h.dia_semana == 'L':
            lunes = 0
        elif h.dia_semana == 'M':
            martes = 1
        elif h.dia_semana == 'X':
            miercoles = 2
        elif h.dia_semana == 'J':
            jueves = 3
        else:
            viernes = 4

    while hoy.day != dossemanas.day:
        d = hoy.weekday()
        if d == lunes or d == martes or d == miercoles or d == jueves or d == viernes:
            lista_dias.append(hoy.date)
        hoy = hoy + mas1dia
    reservas = Reserva.objects.filter(horario__profesor__id=profesor_id).filter(dia__range=[hoy, dossemanas])
    return render_to_response('crearReserva.html', {'lista_dias': lista_dias, 'reservas': reservas,
                                                    'profesor_id': profesor_id}, context)

@user_passes_test(lambda u: not u.es_profesor, login_url='/')
def reservar_tutoria(request):
    context = RequestContext(request)
    form = ReservaTutoriasForm(request.POST)
    if form.is_valid():
        mensajealumno = form.cleaned_data['mensajealumno']
        dia = form.cleaned_data['dia']
        dia = dia.split('-')

        diab =datetime.datetime(int(dia[2]),int(dia[1]),int(dia[0]))
        horario_id = form.cleaned_data['horario_id']
        usuario = request.user
        horario = Horario.objects.get(pk=horario_id)
        reserva = Reserva(estado='P', mensajeAlumno=mensajealumno, mensajeCancel="",dia=diab, alumnos=usuario, horario=horario)
        reserva.save()

        return HttpResponseRedirect(reverse('miPanel'))
    else:
        return render_to_response('crearReserva.html', {'form':form}, context)



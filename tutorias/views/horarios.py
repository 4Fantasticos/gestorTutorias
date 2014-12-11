# encoding:utf-8
__author__ = 'Fran'
import datetime

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from tutorias.models import *
from tutorias.form import *


@user_passes_test(lambda u: u.es_profesor, login_url='/')
def add_horario(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = HorarioForm(request.POST)

        if form.is_valid():
            user = request.user
            dia_semana = form.cleaned_data['dia_semana']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_final = form.cleaned_data['hora_final']
            date_inicio = datetime.datetime.combine(datetime.date.today(), hora_inicio)
            date_fin = datetime.datetime.combine(datetime.date.today(), hora_final)
            _introduce_horario(user, dia_semana, date_inicio, date_fin)
            return HttpResponseRedirect(reverse('miPanel'))
        else:
            return render_to_response('formularioHorario.html', {'form': form}, context)

    form = HorarioForm()
    return render_to_response('formularioHorario.html', {'form': form, 'dias': DIAS_DE_LA_SEMANA}, context)


def _introduce_horario(user, dia_semana, date_inicio, date_fin):
    diff = date_fin - date_inicio
    minutos = diff.total_seconds() / 60
    intervalos = minutos // 15
    mas15 = datetime.timedelta(0, 900)
    for i in range(int(intervalos)):
        horario = Horario(dia_semana=dia_semana, hora_inicio=date_inicio.time(), profesor=user)
        horarios_en_bd = list(Horario.objects.filter(profesor=user).filter(dia_semana=dia_semana).
                              filter(hora_inicio=date_inicio.time))
        if horarios_en_bd == []:
            horario.save()
            date_inicio = date_inicio + mas15


@user_passes_test(lambda u: u.es_profesor, login_url='/')
def eliminar_horario(request, horario_id):
    horario = Horario.objects.filter(profesor=request.user).filter(pk=horario_id)
    horario.delete()
    return HttpResponseRedirect(reverse('misHorarios'))


@user_passes_test(lambda u: u.es_profesor, login_url='/')
def mis_horarios(request):
    context = RequestContext(request)
    user = request.user
    horarios = Horario.objects.filter(profesor=user)
    return render_to_response('misHorarios.html', {'horarios': horarios}, context)


@user_passes_test(lambda u: not u.es_profesor, login_url='/')
def __busca_dia_semana_horario(profesor_id):
    semana = [-1, -1, -1, -1, -1]
    horarios = Horario.objects.filter(profesor=profesor_id)
    for h in horarios:
        if h.dia_semana == 'L':
            semana[0] = 0
        elif h.dia_semana == 'M':
            semana[1] = 1
        elif h.dia_semana == 'X':
            semana[2] = 2
        elif h.dia_semana == 'J':
            semana[3] = 3
        else:
            semana[4] = 4

    return semana


def horarios_profesores(request, profesor_id):
    context = RequestContext(request)
    lista_dias = []
    hoy = datetime.datetime.now()
    mas1dia = datetime.timedelta(1, 0)
    dossemanas = hoy + datetime.timedelta(14, 0)
    semana = __busca_dia_semana_horario(profesor_id)
    while hoy.day != dossemanas.day:
        d = hoy.weekday()
        if d == semana[0] or d == semana[1] or d == semana[2] or d == semana[3] or d == semana[4]:
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

        diab = datetime.datetime(int(dia[2]), int(dia[1]), int(dia[0]))
        horario_id = form.cleaned_data['horario_id']
        usuario = request.user
        horario = Horario.objects.get(pk=horario_id)
        reserva = Reserva(estado='P', mensajeAlumno=mensajealumno, mensajeCancel="", dia=diab, alumnos=usuario,
                          horario=horario)
        reserva.save()

        return HttpResponseRedirect(reverse('miPanel'))
    else:
        return render_to_response('crearReserva.html', {'form': form}, context)

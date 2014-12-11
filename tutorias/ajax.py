# encoding:utf-8
from datetime import datetime
import json
import time

from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User

from tutorias.models import Reserva, Horario


DIAS_DE_LA_SEMANA = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V'}


@dajaxice_register
def gethoras(request, data):
    """
    Metodo ajax para capturar horas

    Este método recibe una fecha y un profesor via json y envia las horas disponibles para esa fecha como objeto json

    :param request: Request
    :param data: Objeto Json con profesor y dia de la semana
    :return: Objeto json con horas de tutoria disponibles para dicho profesor
    """
    dia = time.strptime(data['dia'], '%d-%m-%Y')
    dia_semana = dia.tm_wday
    dia = datetime.fromtimestamp(time.mktime(dia))
    profesor = User.objects.get(pk=data['profesor'])
    reservas = Reserva.objects.filter(horario__profesor=profesor).filter(dia=dia)
    if len(reservas) > 0:
        horas_no = []
        for r in reservas:
            horas_no.append(r.horario.id)
        horarios = Horario.objects.filter(profesor=profesor).filter(dia_semana=DIAS_DE_LA_SEMANA[dia_semana]).exclude(
            pk__in=horas_no)
    else:
        horarios = Horario.objects.filter(profesor=profesor).filter(dia_semana=DIAS_DE_LA_SEMANA[dia_semana])

    enviar = []
    for hora in horarios:
        enviar.append([hora.hora_inicio.strftime("%H:%M"), hora.id])

    data = json.dumps(enviar)
    return data
from datetime import datetime, date
import json
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.core import serializers
import time
from django.db.models import Q
from tutorias.models import Reserva, Horario, Asignatura

DIAS_DE_LA_SEMANA = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V'}


@dajaxice_register
def getHoras(request, data):
    dia = time.strptime(data['dia'], '%d-%m-%Y')
    dia_semana = dia.tm_wday
    dia = datetime.fromtimestamp(time.mktime(dia))
    profesor = User.objects.get(pk=data['profesor'])
    reservas = Reserva.objects.filter(horario__profesor=profesor).filter(dia=dia).filter(Q(estado__exact='P') | Q(estado__exact='R'))
    if len(reservas) > 0:
        horas_no = []
        for r in reservas:
            horas_no.append(r.horario.id)
        horarios = Horario.objects.filter(profesor=profesor).filter(dia_semana=DIAS_DE_LA_SEMANA[dia_semana]).exclude(pk__in=horas_no)
    else:
        horarios = Horario.objects.filter(profesor=profesor).filter(dia_semana=DIAS_DE_LA_SEMANA[dia_semana])

    enviar = []
    for hora in horarios:
        enviar.append([hora.hora_inicio.strftime("%H:%M"),hora.id])

    data = json.dumps(enviar)
    return data
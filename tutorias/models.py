# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password
# Ejemplos sobre relaciones en django
# https://docs.djangoproject.com/en/1.7/topics/db/examples/
# Usuario, extendemos el User por defecto de Django

"""
MODELO USER MODIFICADO
"""
User.add_to_class('dni', models.CharField(max_length=9, unique=True, null=True))
User.add_to_class('es_profesor', models.BooleanField(default=False, blank=True))

"""
MÉTODOS MODELO USER
"""


def getAsignaturas(self):
    lista = self.asignatura_set.all()
    return lista


User.add_to_class('getAsignaturas', getAsignaturas)

"""
MODELO GRADO
"""


class Grado(models.Model):
    titulo = models.CharField(max_length=200)
    identificador = models.CharField(max_length=3)
    usuarios = models.ManyToManyField(User)

    def __unicode__(self):
        return self.titulo

    class Meta:
        ordering = ('titulo',)


"""
MODELO HORARIO
"""
DIAS_DE_LA_SEMANA = (
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
)


class Horario(models.Model):
    profesor = models.ForeignKey(User)
    dia_semana = models.CharField(max_length=1, choices=DIAS_DE_LA_SEMANA)
    hora_inicio = models.TimeField()

    def __unicode__(self):
        return self.profesor.username + " - " + self.dia_semana + " - " + str(self.hora_inicio)

    class Meta:
        ordering = ('dia_semana',)


"""
MODELO ASIGNATURA
"""


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    codigo = models.CharField(max_length=6)
    grados = models.ForeignKey(Grado)
    curso = models.CharField(max_length=1)
    usuarios = models.ManyToManyField(User)

    def __unicode__(self):
        return str(self.codigo) + " - " + self.nombre

    class Meta:
        ordering = ('curso',)


"""
MODELO RESERVA
"""
ESTADO_RESERVA = (
    ('R', 'Reservado'),
    ('L', 'Libre'),
    ('P', 'Pendiente'),
    ('C', 'Cancelada'),
)


class Reserva(models.Model):
    estado = models.CharField(max_length=1, choices=ESTADO_RESERVA)
    mensajeAlumno = models.CharField(max_length=500)
    mensajeCancel = models.CharField(max_length=500, blank=True)
    dia = models.DateField()
    alumnos = models.ForeignKey(User, related_name='alumnos', null=True)
    horario = models.ForeignKey(Horario)
    profesor = models.ForeignKey(User, related_name='profesor', null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        ordering = ('dia',)
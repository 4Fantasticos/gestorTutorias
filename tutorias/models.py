from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
#Ejemplos sobre relaciones en django
#https://docs.djangoproject.com/en/1.7/topics/db/examples/
#Usuario, extendemos el User por defecto de Django

User.add_to_class('dni', models.CharField(max_length=9,unique=True, null=True))
User.add_to_class('es_profesor', models.BooleanField(default=False, blank=True))

class Grado(models.Model):
    titulo = models.CharField(max_length=200)
    identificador = models.CharField(max_length=3)
    usuarios = models.ManyToManyField(User)

    def __unicode__(self):
        return self.titulo
    class Meta:
        ordering = ('titulo',)

DIAS_DE_LA_SEMANA = (
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miercoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
)


class Horario(models.Model):
    profesor = models.ForeignKey(User)
    dia_semana = models.CharField(max_length=1, choices=DIAS_DE_LA_SEMANA)
    hora_inicio = models.DateTimeField()
    
class Asignatura(models.Model):
    codigo = models.CharField(max_length=6)
    grados = models.ForeignKey(Grado)
    curso = models.CharField(max_length=1)
    usuarios = models.ManyToManyField(User)
    class Meta:
        ordering = ('codigo',)

ESTADO_RESERVA = (
    ('R','Reservado'),
    ('L','Libre'),
    ('P','Pendiente'),
)
class Reserva(models.Model):
    estado = models.CharField(max_length=1, choices=ESTADO_RESERVA)
    mensajeAlumno = models.CharField(max_length=500)
    mensajeCancel = models.CharField(max_length=500)
    dia = models.DateField()
    alumnos = models.ForeignKey(User)
    horarios = models.ManyToManyField(Horario)


        
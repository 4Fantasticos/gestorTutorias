# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


User.add_to_class('dni', models.CharField(max_length=9, unique=True, null=True))
User.add_to_class('es_profesor', models.BooleanField(default=False, blank=True))


class Grado(models.Model):
    """
    Modelo de Grado

    :param: titulo: Titulo del grado
    :param: identificador: Identificador único del grado
    :param: usuarios: Lista de usuarios que estudian el grado
    :param: profesores: Lista de profesores que dan el grad
    """
    titulo = models.CharField(max_length=200)
    identificador = models.CharField(max_length=3)
    usuarios = models.ManyToManyField(User, related_name="usuarios")
    profesores = models.ManyToManyField(User, related_name="profesores")

    def __unicode__(self):
        return self.titulo

    class Meta:
        ordering = ('titulo',)


DIAS_DE_LA_SEMANA = (
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
)


class Horario(models.Model):
    """
    Modelo de Horario

    :param: profesor: Profesor de dicho horario
    :param: dia_semana: Día de la semana de la tutoría
    :param: hora_inicio: Hora de inicio de la tutoría
    """
    profesor = models.ForeignKey(User)
    dia_semana = models.CharField(max_length=1, choices=DIAS_DE_LA_SEMANA)
    hora_inicio = models.TimeField()

    def __unicode__(self):
        return self.dia_semana + " - " + str(self.hora_inicio)

    class Meta:
        ordering = ('dia_semana',)


class Asignatura(models.Model):
    """
    Modelo de Asignatura

    :param: nombre: Nombre de la asignatura
    :param: codigo: Código único de la asignatura
    :param: grados: Grado en el cual se imparte la asignatura
    :param: curso: Curso en el cual se imparte la asignatura
    :param: usuarios: Lista de usuarios que dan la asignatura
    :param: profesores: Lista de profesores que dan la asignatura
    """
    nombre = models.CharField(max_length=100, null=True)
    codigo = models.CharField(max_length=6)
    grados = models.ForeignKey(Grado)
    curso = models.CharField(max_length=1)
    usuarios = models.ManyToManyField(User, related_name="usuarios_asignatura")
    profesores = models.ManyToManyField(User, related_name="profesores_asignatura")

    def __unicode__(self):
        return str(self.codigo + " - " + self.nombre)

    class Meta:
        ordering = ('curso',)


ESTADO_RESERVA = (
    ('R', 'Reservado'),
    ('L', 'Libre'),
    ('P', 'Pendiente'),
    ('C', 'Cancelada'),
)


class Reserva(models.Model):
    """
    Modelo de Reserva

    :param: estado: Estado de la reserva
    :param: mensajeAlumno: Mensaje que el alumno deja al profesor
    :param: mensajeCancel: Mensaje que profesor deja para el alumno
    :param: dia: Día de la tutoría
    :param: alumnos: Alumno que pide la tutoría
    :param: horario: Horario del profesor para la tutoría
    """
    estado = models.CharField(max_length=1, choices=ESTADO_RESERVA)
    mensajeAlumno = models.CharField(max_length=500)
    mensajeCancel = models.CharField(max_length=500, blank=True)
    dia = models.DateField()
    alumnos = models.ForeignKey(User, related_name='alumnos', null=True)
    horario = models.ForeignKey(Horario, null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ('dia',)
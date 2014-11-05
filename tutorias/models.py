from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    apellidos = models.CharField(max_length=200, null=False)
    dni = models.CharField(max_length=9, null=False)
    usuario = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=200, null=False)
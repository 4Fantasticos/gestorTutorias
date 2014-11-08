from django.db import models
#Ejemplos sobre relaciones en django
#https://docs.djangoproject.com/en/1.4/topics/db/examples/

class Alumno(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    apellidos = models.CharField(max_length=200, null=False)
    dni = models.CharField(max_length=9, unique=True, null=False)
    usuario = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=200, null=False)

    def __unicode__(self):
    	return self.nombre + " " + self.apellidos
    class Meta:
    	ordering = ('apellidos',)
    		
class Grado(models.Model):
	nombre = models.CharField(max_length=200, null=False)
	alumnos = models.ManyToManyField(Alumno)

	def __unicode__(self):
		return self.nombre
	class Meta:
		ordering = ('nombre',)
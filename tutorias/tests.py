import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client

from tutorias.models import Grado, Asignatura, Reserva


__author__ = 'Laura'


class TestAsignatura(TestCase):
    def setUp(self):
        User.objects.create(username="admin")
        admin = User.objects.get(username="admin")
        admin.set_password("admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        Grado.objects.create(titulo="GIISI", identificador="1")
        grado = Grado.objects.get(titulo="GIISI")

        profesor = User.objects.create(username="profesor")
        profesor.es_profesor = True
        profesor.save()

        alumno = User.objects.create(username="alumno")
        alumno.es_profesor = False
        alumno.save()

        alumno2 = User.objects.create(username="alumno2")
        alumno2.es_profesor = False
        alumno2.save()


        Reserva.objects.create(estado = "P", mensajeAlumno="Tutoria12", dia = datetime.datetime(2014,07,06), alumnos=alumno2)
        Reserva.objects.create(estado = "P", mensajeAlumno="Tutoria22", dia = datetime.datetime(2014,10,11), alumnos=alumno2)

        Reserva.objects.create(estado = "P", mensajeAlumno="Tutoria11", dia = datetime.datetime(2014,03,06), alumnos=alumno)

        Asignatura.objects.create(nombre="Calidad", codigo=1, curso=4, grados=grado)

    def test_add_asignatura(self):
        asignatura = Asignatura.objects.get(codigo=1)
        grado = Grado.objects.get(identificador=1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addAsignatura/',
                          {'nombre': 'Calidad', 'codigo': '1', 'curso': '4', 'grado': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

    def test_remove_asignatura(self):
        self.assertEquals(Asignatura.objects.all().count(), 1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeAsignatura/', {'identificador': '1'})
        boolean = True if 'miPanel' in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(Asignatura.objects.all().count(), 0)

    def test_read_asignatura(self):
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readAsignatura/', {'nombre': 'Calidad'})
        boolean = True if "asignatura" in response.context else False
        self.assertEquals(boolean, True)

    def test_metricas(self):
        c = Client()
        c.login(username="admin", password="admin")
        alumno2 = User.objects.get(username = "alumno2")
        self.assertEquals(Reserva.objects.filter(alumnos=alumno2).count(), 2)
        response = c.post('/admin/estadisticas/', {})
        dic = response.context['alumno_dic']
        self.assertEquals(dic['num'], 2)
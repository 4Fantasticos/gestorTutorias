# encoding:utf-8
import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from tutorias.models import Grado

class GradoViewTestCase(TestCase):
    def setUp(self):
        """
        Iniciación de los requisitos para los test de Grados
        :return: None
        """
        User.objects.create(username="admin")
        admin = User.objects.get(username="admin")
        admin.set_password("admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        Grado.objects.create(titulo="GIISI", identificador="1")
        grado = Grado.objects.get(titulo="GIISI")
        grado.save()

    def test_add_grado(self):
        """
        Metodo que comprueba si se agraga un grado correctamente
        :return: None
        """
        c =Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addGrado/',{'titulo':'GIISI','identificador':'1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean,True)

    def test_remove_grado(self):
        """
        Metodo que comprueba si se elimina un grado correctamente
        :return: None
        """
        self.assertEquals(Grado.objects.all().count(), 1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeGrado/', {'identificador': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(Grado.objects.all().count(), 0)

    def test_read_grado(self):
        """
        Metodo que comprueba si se consulta un grado correctamente
        :return: None
        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readGrado/', {'titulo': 'GIISI'})
        boolean = True if "grado" in response.context else False
        self.assertEquals(boolean, True)


    def test_update_grado(self):
        """
        Metodo que comprueba si se edita un grado correctamente
        :return: None
        """
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateGrado/',{'titulo':'GIISIActualizado','identificador':'1'})
        grado = Grado.objects.get(identificador=1)
        self.assertEquals(grado.titulo,'GIISIActualizado')



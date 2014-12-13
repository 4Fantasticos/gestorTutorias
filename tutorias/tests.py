# encoding:utf-8
import datetime
import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from mixer.backend.django import mixer
from tutorias.models import Horario, Asignatura, Reserva, Grado
from views.horarios import _introduce_horario, _busca_dia_semana_horario
from tutorias.form import *
from tutorias.ajax import gethoras


def inicializacion():
    """
    Iniciación de los requisitos para los test

    """
    User.objects.create(username="profesor", email="profesor@gmail.com", es_profesor=True)
    User.objects.create(username="alumno", email="alumno@gmail.com", es_profesor=False)
    User.objects.create(username="admin")

    profesor = User.objects.get(username="profesor")
    profesor.set_password(1234)
    profesor.save()

    alumno = User.objects.get(username="alumno")
    alumno.set_password(1234)
    alumno.save()

    admin = User.objects.get(username="admin")
    admin.set_password("admin")
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()


class UserTestCase(TestCase):
    """
    Test del modelo User
    """

    def setUp(self):
        """
        Inicialización de las variables necesarias

        """
        inicializacion()

    def test_user(self):
        """
        Los usuarios existen después de crearse

        """
        profesor = User.objects.get(username="profesor")
        alumno = User.objects.get(username="alumno")

        self.assertEquals(profesor.es_profesor, True)
        self.assertEquals(alumno.es_profesor, False)


class GradoTestCase(TestCase):
    """
    Test del modelo Grado
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Grado

        """
        Grado.objects.create(titulo="GIISI", identificador=1)

    def test_grado(self):
        """
        El grado se guarda correctamente

        """
        grado = Grado.objects.get(identificador=1)

        self.assertEquals(grado.titulo, "GIISI")


class HorarioTestCase(TestCase):
    """
    Test del modelo Horario
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Horario

        """
        User.objects.create(username="profesor", email="profesor@gmail.com", es_profesor=True)
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='L', hora_inicio="10:30", profesor=profesor)

    def test_horario(self):
        """
        El horario guarda correctamente el profesor que contiene el horario

        """
        horario = Horario.objects.get(dia_semana='L')
        horario.__unicode__()
        self.assertEquals(horario.profesor.username, "profesor")


class AsignaturaTestCase(TestCase):
    """
    Test del modelo Asignatura
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Asignatura

        """
        User.objects.create(username="profesor", email="profesor@gmail.com", es_profesor=True)
        User.objects.create(username="alumno", email="alumno@gmail.com", es_profesor=False)
        Grado.objects.create(titulo="GIISI", identificador=1)
        profesor = User.objects.get(username="profesor")
        alumno = User.objects.get(username="alumno")
        grado = Grado.objects.get(identificador=1)
        Asignatura.objects.create(nombre="Calidad", codigo=1, grados=grado)
        asignatura = Asignatura.objects.get(codigo=1)
        asignatura.profesores.add(profesor)
        asignatura.usuarios.add(alumno)

    def test_asignatura(self):
        """
        La asignatura guarda correctamente los alummos y profesores que la imparten

        """
        asignatura = Asignatura.objects.get(codigo=1)
        asignatura.__unicode__()
        self.assertEquals(len(asignatura.usuarios.all()), 1)
        self.assertEquals(len(asignatura.profesores.all()), 1)


class ReservaTestCase(TestCase):
    """
    Test del modelo Reserva
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Reserva

        """
        User.objects.create(username="profesor", email="profesor@gmail.com", es_profesor=True)
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='L', hora_inicio="10:30", profesor=profesor)
        horario = Horario.objects.get(dia_semana='L')
        User.objects.create(username="alumno", email="alumno@gmail.com", es_profesor=False)
        alumno = User.objects.get(username="alumno")
        dia = datetime.datetime(2014, 12, 6)
        Reserva.objects.create(estado="P", mensajeAlumno="Necesito tutoría", dia=dia, alumnos=alumno, horario=horario)

    def test_horario(self):
        """
        La reserva se asigna al alumno correctamente.

        """
        reserva = Reserva.objects.get(estado="P")
        reserva.__unicode__()
        self.assertEquals(reserva.alumnos.username, "alumno")


class UsuarioViewTestCase(TestCase):
    """
    Test de las vistas de Usuario
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de User.

        """
        inicializacion()

    def test_login(self):
        """
        Comprobación de la vista user_login

        Comprueba que al no pasarle datos te muestra el login.
        Comprueba que al pasarle usuarios registrados te loguea.
        Comprueba que al ya estar logueado no vuelve a loguear.
        """
        c = Client()

        response = c.get('/', {})
        boolean = True if "miPanel" not in response.context else False
        self.assertEquals(boolean, True)

        response = c.post('/', {'user': 'profesor', 'password': '1234'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

        c.login(username="admin", password="admin")
        response = c.post('/', {'user': 'profesor', 'password': '1234'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

    def test_add_user(self):
        """
        Comprueba la vista add_user

        Comprueba que al agregar corretamente un usuario alumno te envía a agregarle asignaturas.
        Comprueba que al agregar correctamente un usuario profesor te envía a agregarle grados.
        Comprueba que si los datos no son válidos no registra.
        Comprueba que si no se le pasa datos te muestra el formulario.
        """
        Grado.objects.create(titulo="GIISI", identificador=1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addUser/',
                          {'username': 'prueba', 'password': '1234', 'first_name': 'Nombre', 'last_name': 'Apellido',
                           'es_profesor': False, 'dni': '1234567W', 'email': 'prueba@gmail.com', 'grado': '1'})
        boolean = True if "addAsignaturasAlumno" in response.url else False
        self.assertEquals(boolean, True)

        response = c.post('/admin/addUser/',
                          {'username': 'prueba2', 'password': '1234', 'first_name': 'Nom2bre', 'last_name': 'Apelli2do',
                           'es_profesor': True, 'dni': '12345627W', 'email': 'pru2eba@gmail.com', 'grado': '1'})
        boolean = True if "addGradosProfesor" in response.url else False
        self.assertEquals(boolean, True)

        response = c.post('/admin/addUser/',
                          {'userame': 'prueba', 'pasord': '1234', 'fit_name': 'Nombre', 'lastame': 'Apellido',
                           'es_rofesor': True, 'dni': '1234567W', 'emal': 'prueba@gmail.com', 'grao': '1'})
        boolean = True if "grados" in response.context else False
        self.assertEquals(boolean, True)

        response = c.get('/admin/addUser/', {})
        boolean = True if "grados" in response.context else False
        self.assertEquals(boolean, True)

    def test_remove_user(self):
        """
        Comprueba la vista remove_user.

        Comprueba que elimina correctamente un usuario existente.
        Comprueba que si no se le pasa datos te muestra el formulario.
        """
        self.assertEquals(User.objects.all().count(), 3)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeUser/', {'username': 'alumno'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(User.objects.all().count(), 2)

        response = c.post('/admin/removeUser/', {})
        boolean = True if "users" in response.context else False
        self.assertEquals(boolean, True)

    def test_read_user(self):
        """
        Comprueba la vista read_user.

        Comprueba que devuelve el usuario consultado.
        Comprueba que si no se le pasa nada te muestra los usuarios.
        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readUser/', {'username': 'profesor'})
        boolean = True if "profesor" in response.context else True
        self.assertEquals(boolean, True)

        response = c.post('/admin/readUser/', {})
        boolean = True if "usuarios" in response.context else True
        self.assertEquals(boolean, True)

        response = c.get('/admin/readUser/', {'page': '1'})
        boolean = True if "usuarios" in response.context else True
        self.assertEquals(boolean, True)

        response = c.get('/admin/readUser/', {'page': 'asd'})
        boolean = True if "usuarios" in response.context else True
        self.assertEquals(boolean, True)

    def test_update_user(self):
        """
        Comprueba la vista update_user.

        Comprueba que actualiza correctamente un usuario.
        Comprueba que si los datos no son correcto no lo actualiza.
        Comprueba que si no se le pasan datos, te muestra el formulario.
        """
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateUser/',
               {'username': 'alumno', 'password': '1234', 'first_name': 'Actualizado',
                'last_name': 'Apellido',
                'es_profesor': False, 'dni': '1234567W', 'email': 'prueba@gmail.com', 'grado': '1'})
        usuario = User.objects.get(username='alumno')
        self.assertEquals(usuario.first_name, 'Actualizado')

        response = c.post('/admin/updateUser/',
                          {'username': 'alumno', 'password': '1234', 'first_name': 'Actualizado',
                           '123': 'Apellido', 'es_profesor': False, 'dni': '1234567W',
                           'email': 'prueba@gmail.com', 'grado': '1'})
        boolean = True if "usuario" in response.context else True
        self.assertEquals(boolean, True)

        response = c.get('/admin/updateUser/', {'username': 'alumno'})
        boolean = True if "usuario" in response.context else True
        self.assertEquals(boolean, True)

    def test_logout(self):
        """
        Comprueba la vista logout

        Comprueba que elimina la sesion del usuario
        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/logout/', {})
        boolean = True if "/" in response.url else False
        self.assertEquals(boolean, True)

    def test_pedir_tutoria(self):
        """
        Comprueba la vista pedir_tutoria

        Comprueba que muestra las asignaturas al alumno logueado
        """
        c = Client()
        c.login(username="alumno", password="1234")
        al = User.objects.get(username="alumno")
        mixer.blend(Asignatura, usuarios=al, id=666)
        response = c.post('/miPanel/pedirTutoria/', {})
        boolean = True if "profesores" in response.context else False
        self.assertEquals(boolean, True)


class PanelViewTestCase(TestCase):
    """
    Test de las vistas de Panel
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de User

        """
        inicializacion()

    def test_mi_panel(self):
        """
        Comprueba la vista mi_panel

        Comprueba que muestra las reservas del profesor si el usuario es un profesor
        Comprueba que muestra los datos del admin si el usuario es un admin
        Comprueba que muestra las opciones del alumno si el usuario es un alumno
        """
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.post('/miPanel/')
        boolean = True if 'reservas' in response.context['datos'] else False
        self.assertEquals(boolean, True)
        c.logout()

        c.login(username="admin", password="admin")
        response = c.post('/miPanel/')
        boolean = True if 'usuarios' in response.context['datos'] else False
        self.assertEquals(boolean, True)
        c.logout()

        c.login(username="alumno", password="1234")
        response = c.post('/miPanel/')
        boolean = True if 'reservas' in response.context else False
        self.assertEquals(boolean, False)

    def test_add_asignaturas_alumnos(self):
        """
        Comprueba la vista add_asignatura_alumnos

        Comprueba que si no se le pasa nada, se muestra el formulario.
        Comprueba que se dirige a añadir las asignaturas al alumno
        Comprueba que no te dirige a añadir las asignaturas al alumno si los datos no son correctos.
        """
        grado = mixer.blend(Grado, titulo="GIISI", identificador=1)
        alumno = User.objects.get(username="alumno")
        mixer.blend(Asignatura, grados=grado, id=10)
        self.client = Client()
        self.client.login(username="admin", password="admin")
        session = self.client.session
        session['alumno'] = alumno.id
        session['grado'] = 1
        session.save()
        response = self.client.post("/miPanel/addAsignaturasAlumno/", {})
        boolean = True if not response.context['asignaturas'] else False
        self.assertEquals(boolean, False)

        response = self.client.post("/miPanel/addAsignaturasAlumno/", {'choices': 'error'})
        boolean = True if not response.context['asignaturas'] else False
        self.assertEquals(boolean, False)

        response = self.client.post("/miPanel/addAsignaturasAlumno/", {'choices': '10'})
        boolean = True if not response.context else False
        self.assertEquals(boolean, True)

    def test_add_grados_profesor(self):
        """
        Comprueba la vista add_grados_profesor

        Comprueba que si no se le pasan datos muestra el formulario.
        Comprueba que se muestra al añadir un profesor.
        Comprueba que si no se le pasan los datos correctamente no te dirige a añadir los grados.
        """
        profesor = User.objects.get(username="profesor")
        mixer.blend(Grado, profesores=profesor, id=10)
        self.client = Client()
        self.client.login(username="admin", password="admin")
        session = self.client.session
        session['profesor'] = profesor.id
        session.save()
        response = self.client.post("/miPanel/addGradosProfesor/", {})
        boolean = True if not response.context['grados'] else False
        self.assertEquals(boolean, False)

        response = self.client.post("/miPanel/addGradosProfesor/", {'choices': 'error'})
        boolean = True if not response.context['grados'] else False
        self.assertEquals(boolean, False)

        response = self.client.post("/miPanel/addGradosProfesor/", {'choices': '10'})
        boolean = True if not response.context else False
        self.assertEquals(boolean, True)

    def test_add_asignaturas_profesor(self):
        """
        Comprueba la vista add_asignaturas_profesor

        Comprueba que si los datos no son correcto no muestra los grados.
        Comprueba que se muestra al añadir un grado de profesor
        """
        profesor = User.objects.get(username="profesor")
        grado = mixer.blend(Grado, profesores=profesor, titulo="Calidad")
        mixer.blend(Asignatura, grados=grado, id=10)
        self.client = Client()
        self.client.login(username="admin", password="admin")
        session = self.client.session
        session['profesor'] = profesor.id
        session.save()
        response = self.client.post("/miPanel/addAsignaturasProfesor/", {'choices': 'error'})
        boolean = True if not response.context['asignaturas'] else False
        self.assertEquals(boolean, False)
        self.assertEquals(response.context['profesor'], True)

        response = self.client.post("/miPanel/addAsignaturasProfesor/", {'choices': '10'})
        boolean = True if not response.context else False
        self.assertEquals(boolean, True)

    def test_notificaciones_profesor(self):
        """
        Comprueba la vista notificaciones_profesor

        Comprueba que acepta las reservas.
        Comprueba que declina las reservas.
        """
        profesor = User.objects.get(username="profesor")
        mixer.blend(Reserva, profesor=profesor, estado='P', id=1)
        mixer.blend(Reserva, profesor=profesor, estado='P', id=2)
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.post('/miPanel/notificaciones/', {'aceptar': 'aceptar', 'id': '1'})
        boolean = True if not response.context['reservas'] else False
        self.assertEquals(boolean, True)

        response = c.post('/miPanel/notificaciones/', {'declinar': 'declinar', 'id': '2', 'texto': 'qwerty'})
        boolean = True if not response.context['reservas'] else False
        self.assertEquals(boolean, True)

    def test_notificaciones_alumno(self):
        """
        Comprueba la vista notificaciones_alumno

        Comprueba que la vista notificaciones_alumno devuelve las reservas del alumno
        """
        c = Client()
        c.login(username="alumno", password="1234")
        response = c.post('/miPanel/notificacionesAlumno/', {})
        boolean = True if not response.context['reservas'] else False
        self.assertEquals(boolean, True)


class GradoViewTestCase(TestCase):
    """
    Test de las vistas de Grado
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Grados

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
        Comprueba la vista add_grado

        Método que comprueba si se agrega un grado correctamente
        Método que comprueba que si los datos no son correcto, no lo agrega
        Método que comprueba que si no se le pasan datos, te muestra el formulario.
        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addGrado/', {'titulo': 'GIISI', 'identificador': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

        response = c.post('/admin/addGrado/', {'prueba': 'GIISI', 'identificador': '1'})
        boolean = True if "identificador" in response.context['form'] else False
        self.assertEquals(boolean, False)

        response = c.get('/admin/addGrado/', {})
        boolean = True if "form" in response.context else False
        self.assertEquals(boolean, True)

    def test_remove_grado(self):
        """
        Comprueba la vista remove_grado

        Método que comprueba si se elimina un grado correctamente
        Método que comprueba que si no se le pasan datos, muestra el formulario.
        """
        self.assertEquals(Grado.objects.all().count(), 1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeGrado/', {'identificador': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(Grado.objects.all().count(), 0)

        response = c.post('/admin/removeGrado/', {})
        boolean = True if "form" in response.context else False
        self.assertEquals(boolean, True)

    def test_read_grado(self):
        """
        Comprueba la vista read_grado

        Método que comprueba si se consulta un grado correctamente
        Método que comprueba que si no se le pasan datos, muestra el formulario.
        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readGrado/', {'titulo': 'GIISI'})
        boolean = True if "grado" in response.context else False
        self.assertEquals(boolean, True)

        response = c.post('/admin/readGrado/', {})
        boolean = True if "grados" in response.context else False
        self.assertEquals(boolean, True)

    def test_update_grado(self):
        """
        Comprueba la vista update_grado

        Método que comprueba si se edita un grado correctamente
        Método que comprueba si los datos no son correcto no lo añade.
        Método que comprueba si no se le pasan datos, muestra el formulario.
        """
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateGrado/', {'titulo': 'GIISIActualizado', 'identificador': '1'})
        grado = Grado.objects.get(identificador=1)
        self.assertEquals(grado.titulo, 'GIISIActualizado')

        response = c.post('/admin/updateGrado/', {'titu': 'GIISIActualizado', 'identificador': '1'})
        boolean = True if "grado" in response.context else False
        self.assertEquals(boolean, True)

        mixer.blend(Grado, id=10)
        response = c.get('/admin/updateGrado/', {'id': 10})
        boolean = True if "grado" in response.context else False
        self.assertEquals(boolean, True)


class TestAsignatura(TestCase):
    """
    Test de las vistas de Asignatura
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Asignaturas

        Se inicializa todos los objetos que serán necesarios para
        los tests de Asignatura

        """
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

        Reserva.objects.create(estado="P", mensajeAlumno="Tutoria12",
                               dia=datetime.datetime(2014, 07, 06), alumnos=alumno2)
        Reserva.objects.create(estado="P", mensajeAlumno="Tutoria22",
                               dia=datetime.datetime(2014, 10, 11), alumnos=alumno2)

        Reserva.objects.create(estado="P", mensajeAlumno="Tutoria11",
                               dia=datetime.datetime(2014, 03, 06), alumnos=alumno)

        Asignatura.objects.create(nombre="Calidad", codigo=1, curso=4, grados=grado)

    def test_add_asignatura(self):
        """
        Comprueba la vista add_asignatura

        Método que comprueba que se añade una asignatura correctamente
        Método que comprueba que si los datos no son correcto, no añade.
        Método que comprueba que si no se le pasan datos, muestra el formulario.
        """
        Asignatura.objects.get(codigo=1)
        Grado.objects.get(identificador=1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addAsignatura/',
                          {'nombre': 'Calidad', 'codigo': '1', 'curso': '4', 'grado': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

        response = c.post('/admin/addAsignatura/',
                          {'nombr': 'Calidad', 'codigo': '1', 'curso': '4', 'grado': '1'})
        boolean = True if "grados" in response.context else False
        self.assertEquals(boolean, True)

        response = c.get('/admin/addAsignatura/', {})
        boolean = True if "grados" in response.context else False
        self.assertEquals(boolean, True)

    def test_remove_asignatura(self):
        """
        Comprueba la vista remove_asignatura

        Método que comprueba que se elimina una asignatura correctamente
        Método que comprueba que si no se le pasan datos muestra el formulario.
        """
        self.assertEquals(Asignatura.objects.all().count(), 1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeAsignatura/', {'identificador': '1'})
        boolean = True if 'miPanel' in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(Asignatura.objects.all().count(), 0)

        response = c.post('/admin/removeAsignatura/', {})
        boolean = True if 'asignaturas' in response.context else False
        self.assertEquals(boolean, True)

    def test_read_asignatura(self):
        """
        Comprueba la vista read_asignatura

        Método que comprueba que se puede consultar una asignatura correctamente
        Método que comprueba que si no se le pasan datos muestra todas las asignaturas
        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readAsignatura/', {'nombre': 'Calidad'})
        boolean = True if "asignatura" in response.context else False
        self.assertEquals(boolean, True)

        response = c.get('/admin/readAsignatura/', {'page': ''})
        boolean = True if "asignaturas" in response.context else False
        self.assertEquals(boolean, True)

        response = c.get('/admin/readAsignatura/', {'page': '1'})
        boolean = True if "asignaturas" in response.context else False
        self.assertEquals(boolean, True)

        response = c.get('/admin/readAsignatura/', {'page': 'asd'})
        boolean = True if "asignaturas" in response.context else False
        self.assertEquals(boolean, True)

    def test_update_asignatura(self):
        """
        Comprueba la vista update_asignatura

        Método que comprueba que se edite una asignatura correctamente
        Método que comprueba que se si los datos no son correcto no lo actualiza.
        Método que comprueba que si no se le pasa dato, muestra el formulario.
        """
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateAsignatura/', {'nombre': 'Calidad_UPDATE', 'codigo': '1', 'curso': '4', 'grado': '1'})
        asignatura = Asignatura.objects.get(codigo=1)
        self.assertEquals(asignatura.nombre, 'Calidad_UPDATE')

        response = c.post('/admin/updateAsignatura/',
                          {'nomre': 'Calidad_UPDATE', 'codigo': '1', 'curso': '4', 'grado': '1'})
        boolean = True if "asignatura" in response.context else False
        self.assertEquals(boolean, True)

        mixer.blend(Asignatura, id=10)
        response = c.get('/admin/updateAsignatura/', {'id': '10'})
        boolean = True if "asignatura" in response.context else False
        self.assertEquals(boolean, True)

    def test_metricas(self):
        """
        Comprueba la vista métricas

        Método que comprueba que funciona correctamente la métrica del alumno con más números de reservas
        """
        c = Client()
        mixer.blend(Grado)
        mixer.blend(Grado)
        c.login(username="admin", password="admin")
        alumno2 = User.objects.get(username="alumno2")
        self.assertEquals(Reserva.objects.filter(alumnos=alumno2).count(), 2)
        response = c.post('/admin/estadisticas/', {})
        dic = response.context['alumno_dic']
        self.assertEquals(dic['num'], 2)


class TestHorario(TestCase):
    """
    Test del View Horario
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de la vista en la que interviene Horario

        """
        inicializacion()

    def test_add_horario(self):
        """
        Comprueba la vista add_horario

        Comprueba que redirige a miPanel si todo va bien.
        Comprueba que si los datos no son correcto, no añade.
        Comprueba que si no se le pasan datos, muestra el formulario.
        """
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.post('/admin/addHorario/', {'dia_semana': 'L', 'hora_inicio': '10:00', 'hora_final': '10:30'})
        boolean = True if "miPanel" in response.url else False
        self.assertEqual(boolean, True)

        response = c.post('/admin/addHorario/', {'dia_mana': 'L', 'hora_inicio': '10:00', 'hora_final': '10:30'})
        boolean = True if "form" in response.context else False
        self.assertEqual(boolean, True)

        response = c.get('/admin/addHorario/', {})
        boolean = True if "form" in response.context else False
        self.assertEqual(boolean, True)

    def test__introduce_horario(self):
        """
        Comprueba el método auxiliar _introduce_horario

        Comprueba que se crean el numero de intervalos cada 15 minutos y guarda los horarios
        """
        usuario = User.objects.get(username="profesor")
        date_inicio = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 30))
        date_fin = datetime.datetime.combine(datetime.date.today(), datetime.time(11, 00))
        numeroantes = Horario.objects.all().count()
        _introduce_horario(usuario, "L", date_inicio, date_fin)
        numerodespues = Horario.objects.all().count()
        boolean = True if numeroantes + 2 == numerodespues else False
        self.assertEqual(boolean, True)

    def test_eliminar_horario(self):
        """
        Comprueba la vista eliminar_horario

        Comprueba que elimina el horario señalado.
        """
        c = Client()
        c.login(username="profesor", password="1234")
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='L', hora_inicio="12:30", profesor=profesor)
        horario = Horario.objects.filter(dia_semana='L').filter(hora_inicio="12:30").filter(profesor=profesor)
        response = c.post('/miPanel/misHorarios/eliminar/' + str(horario[0].id) + "/", {})
        boolean = True if "misHorarios" in response.url else False
        self.assertEqual(boolean, True)
        horario = Horario.objects.filter(dia_semana='L').filter(hora_inicio="12:30").filter(profesor=profesor)
        boolean = True if not horario else False
        self.assertEqual(boolean, True)

    def test_mis_horario(self):
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.get('/miPanel/misHorarios/', {})
        boolean = True if "horarios" in response.context else False
        self.assertEqual(boolean, True)

    def test__busca_dia_semana_horario(self):
        """
        Comprueba el método auxiliar _busca_dia_semana_horario

        Comprueba que el método auxiliar crea la lista de dias de la semana con tutorias correctamente
        """
        usuario = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='M', hora_inicio="12:30", profesor=usuario)
        mixer.blend(Horario, dia_semana='L', profesor=usuario)
        mixer.blend(Horario, dia_semana='X', profesor=usuario)
        mixer.blend(Horario, dia_semana='J', profesor=usuario)
        mixer.blend(Horario, dia_semana='V', profesor=usuario)
        semana = _busca_dia_semana_horario(usuario.id)
        self.assertEqual(semana[0], 0)
        self.assertEqual(semana[1], 1)
        self.assertEqual(semana[2], 2)
        self.assertEqual(semana[3], 3)
        self.assertEqual(semana[4], 4)

    def test_horarios_profesores(self):
        """
        Comprueba la vista horarios_profesores

        Por cada horario de profesor con dia distinto tenemos dos dias en la lista
        Si creamos una reserva con una fecha pasada el context debe devolver una lista vacia
        """
        c = Client()
        c.login(username="alumno", password="1234")
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='X', hora_inicio="12:30", profesor=profesor)
        Horario.objects.create(dia_semana='J', hora_inicio="12:00", profesor=profesor)
        h1 = Horario.objects.get(dia_semana='X', hora_inicio="12:30", profesor=profesor)
        mixer.blend(Reserva, estado='R', horario=h1, dia='2013-10-10')
        response = c.post('/profesores/' + str(profesor.id) + "/", {})
        profesor_id = response.context['profesor_id']
        lista_dias = response.context['lista_dias']
        reserva = response.context['reservas']
        boolean = True if not reserva else False
        self.assertEqual(boolean, True)
        self.assertEqual(profesor_id, str(profesor.id))
        self.assertEqual(len(lista_dias), 4)

    def test_reservar_tutoria(self):
        """
        Comprueba la vista reservar_tutoria

        Comprueba que redirige a miPanel si todo va bien.
        """
        c = Client()
        c.login(username="alumno", password="1234")
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='X', hora_inicio="20:30", profesor=profesor)
        horario = Horario.objects.get(dia_semana='X', hora_inicio="20:30", profesor=profesor)
        response = c.post('/miPanel/reservarTutoria',
                          {'mensajealumno': 'hola', 'dia': '12-12-2014', 'horario_id': str(horario.id)})

        boolean = True if "miPanel" in response.url else False
        self.assertEqual(boolean, True)

        response = c.post('/miPanel/reservarTutoria',
                          {'mensajelumno': 'hola', 'dia': '12-12-2014', 'horario_id': str(horario.id)})

        boolean = True if "form" in response.context else False
        self.assertEqual(boolean, True)


class FormTest(TestCase):
    """
    Test de los formularios del archivo Form.py
    """

    def test_UserForm(self):
        """
        Comprueba que el form UserForm recibe los datos correctamente.
        Comprueba que el Dni no puede tener más de 10 caracteres.

        """
        form = UserForm(
            {'username': 'Alumno', 'first_name': 'Name', 'last_name': 'LastName', 'email': 'alumno@gmail.com',
             'password': 'Password', 'es_profesor': 'True', 'dni': '1234123'})
        self.assertEquals(form.is_valid(), True)

        form = UserForm(
            {'username': 'Alumno', 'first_name': 'Name', 'last_name': 'LastName', 'email': 'alumno@gmail.com',
             'password': 'Password', 'es_profesor': 'True', 'dni': '123412312123213213123123'})
        self.assertEquals(form.is_valid(), False)

    def test_UserRemoveForm(self):
        """
        Comprueba que el form UserRemoveForm recibe los datos correctamente.

        """
        form = UserRemoveForm({'username': 'Alumno'})
        self.assertEquals(form.is_valid(), True)

    def test_UserReadForm(self):
        """
        Comprueba que el form UserReadForm recibe los datos correctamente.

        """
        form = UserReadForm({'username': 'Alumno'})
        self.assertEquals(form.is_valid(), True)

    def test_UserUpdateForm(self):
        """
        Comprueba que el form UserUpdateForm recibe los datos correctamente.

        """
        form = UserUpdateForm(
            {'username': 'Alumno', 'first_name': 'Name', 'last_name': 'LastName', 'email': 'alumno@gmail.com',
             'password': 'Password', 'es_profesor': 'True', 'dni': '1234123'})
        self.assertEquals(form.is_valid(), True)

    def test_GradoForm(self):
        """
        Comprueba que el form GradoForm recibe los datos correctamente.

        """
        form = GradoForm({'titulo': 'GIISI', 'identificador': '1'})
        self.assertEquals(form.is_valid(), True)

    def test_GradoRemoveForm(self):
        """
        Comprueba que el form GradoRemoveForm recibe los datos correctamente.

        """
        form = GradoRemoveForm({'identificador': '1'})
        self.assertEquals(form.is_valid(), True)

    def test_GradoReadForm(self):
        """
        Comprueba que el form GradoReadForm recibe los datos correctamente.

        """
        form = GradoReadForm({'titulo': 'GIISI'})
        self.assertEquals(form.is_valid(), True)

    def test_GradoUpdateForm(self):
        """
        Comprueba que el form GradoUpdateForm recibe los datos correctamente.

        """
        form = GradoUpdateForm({'titulo': 'GIISI', 'identificador': '1'})
        self.assertEquals(form.is_valid(), True)

    def test_HorarioForm(self):
        """
        Comprueba que el form HorarioForm recibe los datos correctamente.

        Comprueba que la semana tiene que estar dentro del choice, L,M,X,J,V
        Comprueba que la hora de inicio y la hora de fin tiene formato de horas.

        """
        form = HorarioForm({'dia_semana': 'L', 'hora_inicio': '10:30', 'hora_final': '12:30'})
        self.assertEquals(form.is_valid(), True)

        form = HorarioForm({'dia_semana': 'G', 'hora_inicio': '10:30', 'hora_final': '12:30'})
        self.assertEquals(form.is_valid(), False)

        form = HorarioForm({'dia_semana': 'L', 'hora_inicio': '30', 'hora_final': '12:30'})
        self.assertEquals(form.is_valid(), False)

    def test_AsignaturaForm(self):
        """
        Comprueba que el form AsignaturaForm recibe los datos correctamente.

        """
        form = AsignaturaForm({'nombre': 'Calidad', 'codigo': '1', 'curso': '1', 'grado': '1'})
        self.assertEquals(form.is_valid(), True)

    def test_AsignaturaRemoveForm(self):
        """
        Comprueba que el form AsignaturaRemoveForm recibe los datos correctamente.

        """
        form = AsignaturaRemoveForm({'identificador': '1'})
        self.assertEquals(form.is_valid(), True)

    def test_AsignaturaReadForm(self):
        """
        Comprueba que el form AsignaturaReadForm recibe los datos correctamente.

        """
        form = AsignaturaReadForm({'nombre': 'Calidad'})
        self.assertEquals(form.is_valid(), True)

    def test_AsignaturasUpdateForm(self):
        """
        Comprueba que el form AsignaturaupdateForm recibe los datos correctamente.

        """
        form = AsignaturaUpdateForm({'nombre': 'Calidad', 'curso': '1', 'codigo': '12'})
        self.assertEquals(form.is_valid(), True)

    def test_ReservaTutoriasForm(self):
        """
        Comprueba que el form ReservaTutoriasForm recibe los datos correctamente.

        """
        form = ReservaTutoriasForm({'mensajealumno': 'Prueba', 'dia': '3', 'horario_id': '3'})
        self.assertEquals(form.is_valid(), True)


class AjaxTest(TestCase):
    """
    Test que comprueba la funcionalidad ajax de la aplicación

    """

    def setUp(self):
        """
        Inicialización de las variables necesarias

        """
        inicializacion()

    def test_gethoras(self):
        """
        Comprueba que devuelve los json esperados en funcion de los datos de entrada

        """
        profesor = User.objects.get(username="profesor")
        # data diccionario {'alumno': 3, 'profesor': 5, 'dia': u'12-12-2014'}
        horario = mixer.blend(Horario, profesor=profesor, dia_semana='V')
        data = {'alumno': 10, 'profesor': profesor.id, 'dia': '12-12-2014'}
        respuesta = json.loads(gethoras('', data))
        self.assertEquals(profesor.id, respuesta[0][1])
        self.assertEquals(str(horario.hora_inicio)[0:5], respuesta[0][0])
        mixer.blend(Reserva, horario=horario, dia=datetime.date(2014, 12, 12))
        respuesta = json.loads(gethoras('', data))
        boolean = True if not respuesta else False
        self.assertEquals(boolean, True)
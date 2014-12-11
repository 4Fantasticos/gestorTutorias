# encoding:utf-8
import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client

# encoding:utf-8
import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client
from tutorias.models import Grado, Horario, Asignatura, Reserva


def inicializacion():
    """
    Iniciación de los requisitos para los test

    :return: None
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

        :return: None
        """
        inicializacion()

    def test_user_password(self):
        """
        La contraseña debe guardarse bien

        :return:
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

        :return: None
        """
        Grado.objects.create(titulo="GIISI", identificador=1)

    def test_grado(self):
        """
        El grado se guarda correctamente

        :return: None
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

        :return: None
        """
        User.objects.create(username="profesor", email="profesor@gmail.com", es_profesor=True)
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='L', hora_inicio="10:30", profesor=profesor)

    def test_horario(self):
        """
        El horario guarda correctamente el profesor que contiene el horario

        :return: None
        """
        horario = Horario.objects.get(dia_semana='L')
        self.assertEquals(horario.profesor.username, "profesor")


class AsignaturaTestCase(TestCase):
    """
    Test del modelo Asignatura
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Asignatura

        :return: None
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

        :return:
        """
        asignatura = Asignatura.objects.get(codigo=1)
        self.assertEquals(len(asignatura.usuarios.all()), 1)
        self.assertEquals(len(asignatura.profesores.all()), 1)


class ReservaTestCase(TestCase):
    """
    Test del modelo Reserva
    """

    def setUp(self):
        """
        Iniciación de los requisitos para los test de Reserva

        :return: None
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

        :return: None
        """
        reserva = Reserva.objects.get(estado="P")
        self.assertEquals(reserva.alumnos.username, "alumno")


class UsuarioViewTestCase(TestCase):
    def setUp(self):
        """
        Iniciación de los requisitos para los test de User

        :return: None
        """
        inicializacion()

    def test_login(self):
        c = Client()
        response = c.post('/', {'user': 'profesor', 'password': '1234'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

    def test_add_user(self):
        Grado.objects.create(titulo="GIISI", identificador=1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addUser/',
                          {'username': 'prueba', 'password': '1234', 'first_name': 'Nombre', 'last_name': 'Apellido',
                           'es_profesor': False, 'dni': '1234567W', 'email': 'prueba@gmail.com', 'grado': '1'})
        boolean = True if "addAsignaturasAlumno" in response.url else False
        self.assertEquals(boolean, True)

    def test_remove_user(self):
        self.assertEquals(User.objects.all().count(), 3)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeUser/', {'username': 'alumno'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(User.objects.all().count(), 2)

    def test_read_user(self):
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readUser/', {'username': 'profesor'})
        boolean = True if "profesor" in response.context else True
        self.assertEquals(boolean, True)

    def test_update_user(self):
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateUser/',
               {'username': 'alumno', 'password': '1234', 'first_name': 'Actualizado',
                'last_name': 'Apellido',
                'es_profesor': False, 'dni': '1234567W', 'email': 'prueba@gmail.com', 'grado': '1'})
        usuario = User.objects.get(username='alumno')
        self.assertEquals(usuario.first_name, 'Actualizado')

    def test_logout(self):
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/logout/', {})
        boolean = True if "/" in response.url else False
        self.assertEquals(boolean, True)

    def test_pedir_tutoria(self):
        c = Client()
        c.login(username="alumno", password="1234")
        response = c.post('/miPanel/pedirTutoria/', {})
        boolean = True if "misAsignaturas.html" in response.templates[0].name else False
        self.assertEquals(boolean, True)


class PanelViewTestCase(TestCase):
    def setUp(self):
        """
        Iniciación de los requisitos para los test de User

        :return: None
        """
        inicializacion()

    def test_mi_panel(self):
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.post('/miPanel/')
        boolean = True if 'reservas' in response.context['datos'] else False
        self.assertEquals(boolean, True)

    def test_add_asignaturas_alumnos(self):
        Grado.objects.create(titulo="GIISI", identificador=1)
        alumno = User.objects.get(username="alumno")
        self.client = Client()
        self.client.login(username="admin", password="admin")
        session = self.client.session
        session['alumno'] = alumno.id
        session['grado'] = 1
        session.save()
        response = self.client.post("/miPanel/addAsignaturasAlumno/", {})
        boolean = True if not response.context['asignaturas'] else False
        self.assertEquals(boolean, True)

    def test_add_grados_profesor(self):
        profesor = User.objects.get(username="profesor")
        self.client = Client()
        self.client.login(username="admin", password="admin")
        session = self.client.session
        session['profesor'] = profesor.id
        session.save()
        response = self.client.post("/miPanel/addGradosProfesor/", {})
        boolean = True if not response.context['grados'] else False
        self.assertEquals(boolean, True)

    def test_add_asignaturas_profesor(self):
        profesor = User.objects.get(username="profesor")
        self.client = Client()
        self.client.login(username="admin", password="admin")
        session = self.client.session
        session['profesor'] = profesor.id
        session.save()
        response = self.client.post("/miPanel/addAsignaturasProfesor/", {})
        boolean = True if not response.context['asignaturas'] else False
        self.assertEquals(boolean, True)
        self.assertEquals(response.context['profesor'], True)

    def test_notificaciones_profesor(self):
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.post('/miPanel/notificaciones/', {})
        boolean = True if not response.context['reservas'] else False
        self.assertEquals(boolean, True)

    def test_notificaciones_alumno(self):
        c = Client()
        c.login(username="alumno", password="1234")
        response = c.post('/miPanel/notificacionesAlumno/', {})
        boolean = True if not response.context['reservas'] else False
        self.assertEquals(boolean, True)# Create your tests here.
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



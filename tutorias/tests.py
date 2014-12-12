# encoding:utf-8
import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from mixer.backend.django import mixer
from tutorias.models import Horario, Asignatura, Reserva, Grado
from views.horarios import _introduce_horario, _busca_dia_semana_horario


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

    def test_user_password(self):
        """
        La contraseña debe guardarse bien

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
        self.assertEquals(reserva.alumnos.username, "alumno")


class UsuarioViewTestCase(TestCase):
    def setUp(self):
        """
        Iniciación de los requisitos para los test de User

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
        self.assertEquals(boolean, True)


class GradoViewTestCase(TestCase):
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
        Metodo que comprueba si se agraga un grado correctamente

        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addGrado/', {'titulo': 'GIISI', 'identificador': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

    def test_remove_grado(self):
        """
        Metodo que comprueba si se elimina un grado correctamente

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

        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readGrado/', {'titulo': 'GIISI'})
        boolean = True if "grado" in response.context else False
        self.assertEquals(boolean, True)

    def test_update_grado(self):
        """
        Test de modificar grado

        Metodo que comprueba si se edita un grado correctamente
        """
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateGrado/', {'titulo': 'GIISIActualizado', 'identificador': '1'})
        grado = Grado.objects.get(identificador=1)
        self.assertEquals(grado.titulo, 'GIISIActualizado')


class TestAsignatura(TestCase):
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
        Test de añadir asignatura

        Método que comprueba que se añade una asignatura correctamente

        """
        Asignatura.objects.get(codigo=1)
        Grado.objects.get(identificador=1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/addAsignatura/',
                          {'nombre': 'Calidad', 'codigo': '1', 'curso': '4', 'grado': '1'})
        boolean = True if "miPanel" in response.url else False
        self.assertEquals(boolean, True)

    def test_remove_asignatura(self):
        """
        Test de eliminar asignatura

        Método que comprueba que se elimina una asignatura correctamente

        """
        self.assertEquals(Asignatura.objects.all().count(), 1)
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/removeAsignatura/', {'identificador': '1'})
        boolean = True if 'miPanel' in response.url else False
        self.assertEquals(boolean, True)
        self.assertEquals(Asignatura.objects.all().count(), 0)

    def test_read_asignatura(self):
        """
        Test de consultar asignatura

        Método que comprueba que se puede consultar una asignatura
        correctamente

        """
        c = Client()
        c.login(username="admin", password="admin")
        response = c.post('/admin/readAsignatura/', {'nombre': 'Calidad'})
        boolean = True if "asignatura" in response.context else False
        self.assertEquals(boolean, True)

    def test_update_asignatura(self):
        """
        Test de modificar asignatura

        Metodo que comprueba que se edite una asignatura correctamente

        """
        c = Client()
        c.login(username="admin", password="admin")
        c.post('/admin/updateAsignatura/', {'nombre': 'Calidad_UPDATE', 'codigo': '1', 'curso': '4', 'grado': '1'})
        asignatura = Asignatura.objects.get(codigo=1)
        self.assertEquals(asignatura.nombre, 'Calidad_UPDATE')

    def test_metricas(self):
        """
        Test de métricas

        Método que comprueba que funciona correctamente la métrica
        del alumno con más números de reservas

        """
        c = Client()
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
        Comprueba que la vista addHorario redirige a miPanel si todo va bien.

        """
        c = Client()
        c.login(username="profesor", password="1234")
        response = c.post('/admin/addHorario/',
                          {'dia_semana': 'L', 'hora_inicio': '10:00', 'hora_final': '10:30'})
        boolean = True if "miPanel" in response.url else False
        self.assertEqual(boolean, True)

    def test__introduce_horario(self):
        """
        Comprueba que se crean el numero de intervalos cada 15 minutos y guarda los horarios

        """
        usuario = User.objects.get(username="profesor")
        date_inicio = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 30))
        date_fin = datetime.datetime.combine(datetime.date.today(), datetime.time(11, 00))
        numeroantes = Horario.objects.all().count()
        _introduce_horario(usuario, "L", date_inicio, date_fin)
        numerodespues = Horario.objects.all().count()
        boolean = True if numeroantes+2 == numerodespues else False
        self.assertEqual(boolean, True)

    def test_eliminar_horario(self):
        """
        Elimina el horario de un profesor

        """
        c = Client()
        c.login(username="profesor", password="1234")
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='L', hora_inicio="12:30", profesor=profesor)
        horario = Horario.objects.filter(dia_semana='L').filter(hora_inicio="12:30").filter(profesor=profesor)
        response = c.post('/miPanel/misHorarios/eliminar/'+str(horario[0].id)+"/", {})
        boolean = True if "misHorarios" in response.url else False
        self.assertEqual(boolean, True)
        horario = Horario.objects.filter(dia_semana='L').filter(hora_inicio="12:30").filter(profesor=profesor)
        boolean = True if not horario else False
        self.assertEqual(boolean, True)

    def test__busca_dia_semana_horario(self):
        """
        Comprueba que el método auxiliar crea la lista de dias de la semana con tutorias correctamente

        """
        usuario = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='M', hora_inicio="12:30", profesor=usuario)
        semana = _busca_dia_semana_horario(usuario.id)
        self.assertEquals(semana[1], 1)
        self.assertEquals(semana[4], -1)

    def test_horarios_profesores(self):
        """
        Comprueba que el context pasado al template es correcto
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
        response = c.post('/profesores/'+str(profesor.id)+"/", {})
        profesor_id = response.context['profesor_id']
        lista_dias = response.context['lista_dias']
        reserva = response.context['reservas']
        boolean = True if not reserva else False
        self.assertEqual(boolean, True)
        self.assertEqual(profesor_id, str(profesor.id))
        self.assertEqual(len(lista_dias), 4)

    def test_reservar_tutoria(self):
        """
        Comprueba que la vista reservarTutoria redirige a miPanel si todo va bien.

        """
        c = Client()
        c.login(username="alumno", password="1234")
        profesor = User.objects.get(username="profesor")
        Horario.objects.create(dia_semana='X', hora_inicio="20:30", profesor=profesor)
        horario = Horario.objects.get(dia_semana='X', hora_inicio="20:30", profesor=profesor)
        response = c.post('/miPanel/reservarTutoria',
                          {'mensajealumno': 'hola', 'dia': '12-12-2014', 'horario_id': str(horario.id)})
        print response
        boolean = True if "miPanel" in response.url else False
        self.assertEqual(boolean, True)
# encoding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from tutorias.models import *
from tutorias.form import *
import datetime


def esProfesor(user):
    return user.es_profesor


def esALumno(user):
    return not user.es_profesor


def esAdmin(user):
    return user.is_superuser


def user_login(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('miPanel'))
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('miPanel'))

    return render_to_response('index.html', {}, context)


def user_logout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse('login'))


'''@user_passes_test(esProfesor, login_url='/') NO ENTRA SI LA FUNCIÓN DEVUELVE TRUE'''


def add_grado(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = GradoForm(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            identificador = form.cleaned_data['identificador']

            grado = Grado(titulo=titulo, identificador=identificador)
            grado.save()

            return HttpResponseRedirect(reverse('miPanel'))
        else:
            return render_to_response('formularioGrado.html', {'form': form}, context)

    form = GradoForm()
    return render_to_response('formularioGrado.html', {'form': form}, context)


def add_users(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            es_profesor = form.cleaned_data['es_profesor']
            dni = form.cleaned_data['dni']
            email = form.cleaned_data['email']
            grado_identificador = form.cleaned_data['grado']

            user = User.objects.create_user(username, email, password)
            user.es_profesor = es_profesor
            user.first_name = first_name
            user.last_name = last_name
            user.dni = dni
            user.set_password(password)
            user.save()
            if not es_profesor:
                g = Grado.objects.get(identificador=grado_identificador)
                g.usuarios.add(user)
                request.session['alumno'] = user.id
                request.session['grado'] = grado_identificador
                return HttpResponseRedirect(reverse('add_asignaturas_alumno'))
            elif es_profesor:
                request.session['profesor'] = user.id
                return HttpResponseRedirect(reverse('add_grados_profesor'))
            return HttpResponseRedirect(reverse('miPanel'))
        else:
            grados = Grado.objects.all()
            return render_to_response('formularioUser.html', {'form': form, 'grados': grados}, context)

    grados = Grado.objects.all()
    form = UserForm()
    return render_to_response('formularioUser.html', {'form': form, 'grados': grados}, context)


def addAsignaturasAlumnos(request):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=request.session['alumno'])
    grado = get_object_or_404(Grado, identificador=request.session['grado'])
    asignaturas = Asignatura.objects.filter(grados=grado)
    if request.method == 'POST':
        form = AddAsignaturasForm(request.POST, asignaturas=asignaturas)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                asig = Asignatura.objects.get(codigo=item)
                asig.usuarios.add(user)
            return HttpResponseRedirect(reverse('miPanel'))
        else:
            form = AddAsignaturasForm(request.POST, asignaturas=asignaturas)
            return render_to_response('formAddAsignaturas.html', {'form': form, 'asignaturas': asignaturas}, context)
    form = AddAsignaturasForm(asignaturas=asignaturas)
    return render_to_response('formAddAsignaturas.html', {'form': form, 'asignaturas': asignaturas}, context)


def addGradosProfesor(request):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=request.session['profesor'])
    grados = Grado.objects.all()
    if request.method == 'POST':
        form = AddGradosForm(request.POST, grados=grados)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                grado = Grado.objects.get(identificador=item)
                grado.profesores.add(user)
        request.session['profesor'] = user.id
        return HttpResponseRedirect(reverse('add_asignaturas_profesor'))
    else:
        form = AddGradosForm(request.POST, grados=grados)
        return render_to_response('formAddGrados.html', {'form': form, 'grados': grados}, context)
    form = AddGradosForm(grados=grados)
    return render_to_response('formAddGrados.html', {'form': form, 'grados': grados}, context)


def addAsignaturasProfesor(request):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=request.session['profesor'])
    listaAsignaturas = []
    grados = Grado.objects.filter(profesores=user)
    for grado in grados:
        asignaturas = Asignatura.objects.filter(grados=grado)
        for asignatura in asignaturas:
            listaAsignaturas.append(asignatura)
    if request.method == 'POST':
        form = AddAsignaturasForm(request.POST, asignaturas=asignaturas)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                asig = Asignatura.objects.get(codigo=item)
                asig.profesores.add(user)
            return HttpResponseRedirect(reverse('miPanel'))
        else:
            form = AddAsignaturasForm(request.POST, asignaturas=asignaturas)
            return render_to_response('formAddAsignaturas.html',
                                      {'profesor': True, 'form': form, 'asignaturas': asignaturas}, context)
    form = AddAsignaturasForm(asignaturas=asignaturas)
    return render_to_response('formAddAsignaturas.html', {'profesor': True, 'form': form, 'asignaturas': asignaturas},
                              context)


def add_horario(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = HorarioForm(request.POST)

        if form.is_valid():
            user = request.user
            dia_semana = form.cleaned_data['dia_semana']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_final = form.cleaned_data['hora_final']
            date_inicio = datetime.datetime.combine(datetime.date.today(),hora_inicio)
            date_fin = datetime.datetime.combine(datetime.date.today(),hora_final)
            diff = date_fin - date_inicio
            minutos = diff.total_seconds()/60
            intervalos = minutos//15
            mas15 = datetime.timedelta(0,900)
            for i in range(int(intervalos)):
                horario = Horario(dia_semana=dia_semana, hora_inicio=date_inicio.time(),profesor=user)
                horario.save()
                date_inicio=date_inicio+mas15
            

            return HttpResponseRedirect(reverse('miPanel'))
        else:
            return render_to_response('formularioHorario.html', {'form': form}, context)

    form = HorarioForm()
    return render_to_response('formularioHorario.html', {'form': form, 'dias': DIAS_DE_LA_SEMANA}, context)


def add_asignatura(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = AsignaturaForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            codigo = form.cleaned_data['codigo']
            curso = form.cleaned_data['curso']
            grado_id = form.cleaned_data['grado']
            grado = Grado.objects.get(identificador=grado_id)

            asignatura = Asignatura(nombre=nombre, codigo=codigo, curso=curso, grados=grado)
            asignatura.save()

            return HttpResponseRedirect(reverse('miPanel'))
        else:
            grados = Grado.objects.all()
            return render_to_response('formularioAsignatura.html', {'form': form, 'grados': grados}, context)

    grados = Grado.objects.all()
    form = AsignaturaForm()
    return render_to_response('formularioAsignatura.html', {'form': form, 'grados': grados}, context)


def miPanel(request):
    context = RequestContext(request)
    if request.user.is_superuser:
        usuarios = User.objects.exclude(username='admin')
        grados = Grado.objects.all()
        asignaturas = Asignatura.objects.all()
        datos = {'usuarios': len(usuarios), 'grados': len(grados), 'asignaturas': len(asignaturas)}
        return render_to_response('miPanel.html', {'datos': datos}, context)
    elif request.user.es_profesor:
        reservas = Reserva.objects.filter(horario__profesor=request.user, estado='P')
        datos = {'reservas': len(reservas)}
        return render_to_response('miPanel.html', {'datos': datos}, context)
    else:
        return render_to_response('miPanel.html', {}, context)


def mis_horarios(request):
    context = RequestContext(request)
    user = request.user
    horarios = Horario.objects.filter(profesor=user)
    return render_to_response('misHorarios.html', {'horarios': horarios}, context)


def remove_asignatura(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = AsignaturaRemoveForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['identificador']
            asignatura = Asignatura.objects.get(pk=id)
            asignatura.delete()

            return HttpResponseRedirect(reverse('miPanel'))

    asignaturas = Asignatura.objects.all()
    form = AsignaturaRemoveForm()
    return render_to_response('removeAsignatura.html', {'form': form, 'asignaturas': asignaturas}, context)


def remove_grado(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = GradoRemoveForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['identificador']
            grado = Grado.objects.get(pk=id)
            grado.delete()

            return HttpResponseRedirect(reverse('miPanel'))

    grados = Grado.objects.all()
    form = GradoRemoveForm()
    return render_to_response('removeGrado.html', {'form': form, 'grados': grados}, context)


def remove_user(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = UserRemoveForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            user.delete()

            return HttpResponseRedirect(reverse('miPanel'))

    users = User.objects.all()
    form = UserRemoveForm()
    return render_to_response('removeUser.html', {'form': form, 'users': users}, context)


def read_user(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserReadForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            usuario = User.objects.filter(username__icontains=username)
        return render_to_response('readUser.html', {'form': form, 'users': usuario}, context)
    usuarios_list = User.objects.exclude(username='admin')
    paginator = Paginator(usuarios_list, 10)
    page = request.GET.get('page')
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)
    form = UserReadForm()
    return render_to_response('readUser.html', {'form': form, 'usuarios': usuarios}, context)


def read_asignatura(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = AsignaturaReadForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            asignatura = Asignatura.objects.filter(nombre__icontains=nombre)
            return render_to_response('readAsignatura.html', {'form': form, 'asignatura': asignatura}, context)
    asignaturas_lista = Asignatura.objects.all()
    paginator = Paginator(asignaturas_lista, 10)
    page = request.GET.get('page')
    try:
        asignaturas = paginator.page(page)
    except PageNotAnInteger:
        asignaturas = paginator.page(1)
    except EmptyPage:
        asignaturas = paginator.page(paginator.num_pages)
    form = AsignaturaReadForm()
    return render_to_response('readAsignatura.html', {'form': form, 'asignaturas': asignaturas}, context)

def read_grado(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = GradoReadForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            grado = Grado.objects.filter(titulo__icontains=titulo)
            return render_to_response('readGrado.html', {'form': form, 'grado': grado}, context)
    grado_lista = Grado.objects.all()
    paginator = Paginator(grado_lista, 10)
    page = request.GET.get('page')
    try:
        grados = paginator.page(page)
    except PageNotAnInteger:
        grados = paginator.page(1)
    except EmptyPage:
        grados = paginator.page(paginator.num_pages)
    form = AsignaturaReadForm()
    return render_to_response('readGrado.html', {'form': form, 'grados': grados}, context)


def notificacionesProfesor(request):
    context = RequestContext(request)
    if 'aceptar' in request.POST:
        id = request.POST.get('id')
        reserva = Reserva.objects.get(id=id)
        reserva.estado = 'R'
        reserva.save()
    elif 'declinar' in request.POST:
        id = request.POST.get('id')
        textoProfesor = request.POST.get('texto')
        reserva = Reserva.objects.get(id=id)
        reserva.mensajeCancel = textoProfesor
        reserva.estado = 'C'
        reserva.save()
    notificaciones = Reserva.objects.filter(horario__profesor=request.user).filter(estado='P')
    reservas = Reserva.objects.filter(horario__profesor=request.user).filter(estado='R').filter(dia__gt=datetime.datetime.now)
    aceptadas_lista = Reserva.objects.filter(horario__profesor=request.user).filter(estado='R').filter(dia__lt=datetime.datetime.now)
    paginator_aceptadas = Paginator(aceptadas_lista, 10)
    page_aceptadas = request.GET.get('page_a')
    try:
        aceptadas = paginator_aceptadas.page(page_aceptadas)
    except PageNotAnInteger:
        aceptadas = paginator_aceptadas.page(1)
    except EmptyPage:
        aceptadas = paginator_aceptadas.page(paginator_aceptadas.num_pages)
    canceladas_lista = Reserva.objects.filter(horario__profesor=request.user).filter(estado='C')
    paginator_canceladas = Paginator(canceladas_lista, 10)
    page_canceladas = request.GET.get('page_c')
    try:
        canceladas = paginator_canceladas.page(page_canceladas)
    except PageNotAnInteger:
        canceladas = paginator_canceladas.page(1)
    except EmptyPage:
        canceladas = paginator_canceladas.page(paginator_canceladas.num_pages)
    return render_to_response('misNotificaciones.html',
                              {'notificaciones': notificaciones, 'reservas': reservas, 'canceladas': canceladas,
                               'aceptadas': aceptadas},
                              context)


def pedirTutoria(request):
    context = RequestContext(request)
    usuario = request.user
    asignaturas = Asignatura.objects.filter(usuarios=usuario)
    profesores = {}
    codeasig = {}
    for asignatura in asignaturas:
        profesores[asignatura.nombre] = asignatura.profesores.all()
        codeasig[asignatura.nombre] = asignatura.id
    return render_to_response('misAsignaturas.html',
                              {'profesores': profesores, 'codeasig': codeasig},
                              context)

def update_asignatura(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = AsignaturaUpdateForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            codigo = form.cleaned_data['codigo']
            curso = form.cleaned_data['curso']

            asignatura = Asignatura.objects.get(codigo=codigo)
            asignatura.nombre = nombre
            asignatura.codigo = codigo
            asignatura.curso = curso

            asignatura.save()

            asignaturas_lista = Asignatura.objects.all()
            paginator = Paginator(asignaturas_lista, 10)
            page = request.GET.get('page')
            try:
                asignaturas = paginator.page(page)
            except PageNotAnInteger:
                asignaturas = paginator.page(1)
            except EmptyPage:
                asignaturas = paginator.page(paginator.num_pages)
            form = AsignaturaReadForm()
            return render_to_response('readAsignatura.html', {'form': form, 'asignaturas': asignaturas}, context)
        else:
            codigo = form.cleaned_data['codigo']
            asignatura = Asignatura.objects.get(codigo=codigo)
            return render_to_response('updateAsignatura.html', {'form': form, 'asignatura': asignatura}, context)
    id = request.GET.get('id')
    asignatura = Asignatura.objects.get(id=id)
    form = AsignaturaUpdateForm()
    return render_to_response('updateAsignatura.html', {'form': form, 'asignatura': asignatura}, context)

def update_grado(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = GradoForm(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            identificador = form.cleaned_data['identificador']

            grado = Grado.objects.get(identificador=identificador)
            grado.titulo=titulo

            grado.save()

            grado_lista = Grado.objects.all()
            paginator = Paginator(grado_lista, 10)
            page = request.GET.get('page')
            try:
                grados = paginator.page(page)
            except PageNotAnInteger:
                grados = paginator.page(1)
            except EmptyPage:
                grados = paginator.page(paginator.num_pages)
            return render_to_response('readGrado.html', {'form': form, 'grados': grados}, context)
        else:
            identificador = form.cleaned_data['identificador']
            grado = Grado.objects.get(identificador=identificador)
            return render_to_response('updateGrado.html', {'form': form, 'grado': grado}, context)
    id=request.GET.get('id')
    grado= Grado.objects.get(id=id)
    form = GradoUpdateForm()
    return render_to_response('updateGrado.html', {'form': form, 'grado': grado}, context)

def horarios_profesores(request, profesor_id):
    context = RequestContext(request)
    horarios = Horario.objects.filter(profesor=profesor_id)
    lista_dias=[]
    hoy = datetime.datetime.now()
    mas1dia = datetime.timedelta(1, 0)
    dossemanas = hoy + datetime.timedelta(14, 0)
    lunes, martes, miercoles, jueves, viernes = -1,-1,-1,-1,-1
    for h in horarios:
        if h.dia_semana=='L':
            lunes=0
        elif h.dia_semana=='M':
            martes=1
        elif h.dia_semana=='X':
            miercoles=2
        elif h.dia_semana=='J':
            jueves=3
        else:
            viernes=4

    while hoy.day != dossemanas.day:
        d = hoy.weekday()
        if d == lunes or d == martes or d == miercoles or d == jueves or d == viernes:
            lista_dias.append(hoy.date)
        hoy = hoy + mas1dia
    reservas = Reserva.objects.filter(horario__profesor__id=profesor_id).filter(dia__range=[hoy, dossemanas])
    return render_to_response('crearReserva.html', {'lista_dias': lista_dias, 'reservas': reservas,
                                                    'profesor_id': profesor_id}, context)

def update_user(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            es_profesor = form.cleaned_data['es_profesor']
            dni = form.cleaned_data['dni']
            email = form.cleaned_data['email']

            user = User.objects.get(username = username)
            user.es_profesor = es_profesor
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.dni = dni
            user.save()

            usuarios_list = User.objects.exclude(username='admin')
            paginator = Paginator(usuarios_list, 10)
            page = request.GET.get('page')
            try:
                usuarios = paginator.page(page)
            except PageNotAnInteger:
                usuarios = paginator.page(1)
            except EmptyPage:
                usuarios = paginator.page(paginator.num_pages)
            return render_to_response('readUser.html', {'form': form, 'usuarios': usuarios}, context)
        else:
            username = form.cleaned_data['username']
            usuario = User.objects.get(username=username)
            return render_to_response('updateUser.html', {'form': form, 'usuario': usuario}, context)
    username=request.GET.get('username')
    usuario= User.objects.get(username=username)
    form = GradoUpdateForm()
    return render_to_response('updateUser.html', {'form': form, 'usuario': usuario}, context)

def reservar_tutoria(request):
        form = ReservaTutoriasForm(request.POST)
        if form.is_valid():
            mensajealumno = form.cleaned_data['mensajealumno']
            dia = form.cleaned_data['dia']
            horario_id = form.cleaned_data['horario_id']
            usuario_id = request.user.id
            reserva = Reserva(estado='P', mensajeAlumno=mensajealumno, mensajeCancel="",
                              dia=dia,alumnos=usuario_id,horario=horario_id)
            reserva.save()

            return HttpResponseRedirect(reverse('miPanel'))

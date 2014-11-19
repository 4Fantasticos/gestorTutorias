# encoding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from tutorias.models import *
from tutorias.form import *


def esProfesor(user):
    return user.es_profesor


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
                user.grado_set.add(g)
                request.session['alumno'] = user.id
                request.session['grado'] = grado_identificador
                return HttpResponseRedirect(reverse('add_asignaturas_alumno'))
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
    if request.method == 'POST':
        form = AddAsignaturasForm(request.POST)
        if form.is_valid():
            for item in form.cleaned_data['choices']:
                user.asignatura_set.add(item)
            return HttpResponse("OK")
        else:
            asignaturas = Asignatura.objects.filter(grados=grado)
            return render_to_response('formAddAsignaturas.html', {'form': form, 'asignaturas': asignaturas}, context)
    asignaturas = Asignatura.objects.filter(grados=grado)
    form = AddAsignaturasForm()
    return render_to_response('formAddAsignaturas.html', {'form': form, 'asignaturas': asignaturas}, context)

def add_horario(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = HorarioForm(request.POST)

        if form.is_valid():
            user = request.user
            dia_semana = form.cleaned_data['dia_semana']
            hora_inicio = form.cleaned_data['hora_inicio']

            horario = Horario(dia_semana=dia_semana, hora_inicio=hora_inicio, profesor=user)
            horario.save()

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
    return render_to_response('miPanel.html', {}, context)

def mis_horarios(request):
    context = RequestContext(request)
    user = request.user
    horarios = Horario.objects.filter(profesor=user)
    return render_to_response('misHorarios.html', {'horarios':horarios}, context)
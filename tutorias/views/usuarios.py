# encoding:utf-8
__author__ = 'Sergio'
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from tutorias.models import *
from tutorias.form import *


def user_login(request):
    """
    Vista de login del usuario

    El siguiente método recoge vía request los parametros de un form, los evalua y logea al usuario si procede, en caso
    contrario deriva al template index.html

    :param request: Request
    :return: A la vista index.html
    """
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('miPanel'))
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('miPanel'))

    return render_to_response('index.html', {}, context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def add_users(request):
    """
    Vista añadir usuario.

    El siguiente método recoge vía request los parametros de un form, los evalua y añade un usuario si procede, en caso
    contrario deriva al template formularioUser.html

    :param request: Request
    :return: Al formulario formularioUser.html
    """
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def remove_user(request):
    """
    Elimina un usuario del sistema.

    El siguiente método recoge vía request los parametros de un form, los evalua y elimina un usuario si procede, en
    caso contrario deriva al template removeUser.html

    :param request: request
    :return: Vista removeUser.html
    """
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def read_user(request):
    """
    Consultar un usuario del sistema.

    El siguiente método recoge vía request los parametros de un form, los evalua y muestra los datos de un usuario si
    procede, en caso contrario deriva al template readUser.html

    :param request: request
    :return: Vista readUser.html
    """
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserReadForm(request.POST)
        usuario = None
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def update_user(request):
    """
    Modifica mina un usuario del sistema.

    El siguiente método recoge vía request los parametros de un form, los evalua y modifica un usuario si procede, en
    caso contrario deriva al template updateUser.html

    :param request: request
    :return: Vista updateUser.html
    """
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

            user = User.objects.get(username=username)
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
    username = request.GET.get('username')
    usuario = User.objects.get(username=username)
    form = GradoUpdateForm()
    return render_to_response('updateUser.html', {'form': form, 'usuario': usuario}, context)


def user_logout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse('login'))


@user_passes_test(lambda u: not u.es_profesor, login_url='/')
def pedir_tutoria(request):
    """
    Pedir tutoría a un profesor.

    El siguiente método recoge vía request los parametros de un form, los evalua y crea una tutoria si procede, en
    caso contrario deriva al template misAsignaturas.html

    :param request: request
    :return: Vista misAsignaturas.html
    """
    context = RequestContext(request)
    usuario = request.user
    asignaturas = Asignatura.objects.filter(usuarios=usuario)
    profesores = {}
    codeasig = {}
    for asignatura in asignaturas:
        profesores[asignatura.nombre] = asignatura.profesores.all()
        codeasig[asignatura.nombre] = asignatura.id
    return render_to_response('misAsignaturas.html', {'profesores': profesores, 'codeasig': codeasig}, context)
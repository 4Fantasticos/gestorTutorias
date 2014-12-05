__author__ = 'usuario'
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from tutorias.models import *
from tutorias.form import *


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def add_grado(request):
    """ Vista añadir grado

    El siguiente método recoge vía request los parametros de un form, los evalua y añade un grado si procede, en caso
    contrario deriva al template formularioGrado.html

    :param request: Request.
    :return: formularioGrado.html.
    """
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def remove_grado(request):
    """Elimina un grado del sistema

    El siguiente método recoge vía request los parametros de un form, los evalua y elimina un grado si procede, en
    caso contrario deriva al template removeGrado.html.

    :param request: request
    :return: Vista removeGrado.html
    """
    context = RequestContext(request)

    if request.method == 'POST':
        form = GradoRemoveForm(request.POST)

        if form.is_valid():
            identificador = form.cleaned_data['identificador']
            grado = Grado.objects.get(pk=identificador)
            grado.delete()

            return HttpResponseRedirect(reverse('miPanel'))

    grados = Grado.objects.all()
    form = GradoRemoveForm()
    return render_to_response('removeGrado.html', {'form': form, 'grados': grados}, context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def read_grado(request):
    """Consultar un grado del sistema.

    El siguiente método recoge vía request los parametros de un form, los evalua y muestra los datos de un grado si
    procede, en caso contrario deriva al template readGrado.html

    :param request: request
    :return: Vista readGrado.html
    """
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def update_grado(request):
    """Modifica un grado del sistema.

    El siguiente método recoge vía request los parametros de un form, los evalua y modifica un grado si procede, en
    caso contrario deriva al template updateGrado.html

    :param request: request
    :return: Vista updateGrado.html
    """
    context = RequestContext(request)

    if request.method == 'POST':
        form = GradoForm(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            identificador = form.cleaned_data['identificador']

            grado = Grado.objects.get(identificador=identificador)
            grado.titulo = titulo

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
    identificador = request.GET.get('id')
    grado = Grado.objects.get(id=identificador)
    form = GradoUpdateForm()
    return render_to_response('updateGrado.html', {'form': form, 'grado': grado}, context)


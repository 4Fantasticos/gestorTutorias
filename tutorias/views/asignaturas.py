# encoding:utf-8
__author__ = 'Laura'
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from tutorias.models import *
from tutorias.form import *


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def add_asignatura(request):
    """
    Añadir asignatura

    El siguiente método recoge vía request los parametros de un form,
    los evalua y crea una asignatura si procede, en caso contrario
    deriva al template formularioAsignatura.html

    :param request: request
    :return: Vista de miPanel o de formularioAsignatura.html si algo falla
    """
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def remove_asignatura(request):
    """
    Eliminar asignatura

    El siguiente método recoge vía request los parametros de un form,
    los evalua y elimina una asignatura

    :param request: request
    :return: Vista de miPanel
    """
    context = RequestContext(request)

    if request.method == 'POST':
        form = AsignaturaRemoveForm(request.POST)

        if form.is_valid():
            id_asignatura = form.cleaned_data['identificador']
            asignatura = Asignatura.objects.get(pk=id_asignatura)
            asignatura.delete()

            return HttpResponseRedirect(reverse('miPanel'))

    asignaturas = Asignatura.objects.all()
    form = AsignaturaRemoveForm()
    return render_to_response('removeAsignatura.html', {'form': form, 'asignaturas': asignaturas}, context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def read_asignatura(request):
    """
    Consultar asignatura

    El siguiente método recoge vía request los parametros de un form,
    los evalua y muestra una asignatura

    :param request: request
    :return: Vista de readAsignatura.html si algo falla
    """
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
    form = AsignaturaReadForm()
    return render_to_response('readAsignatura.html', {'form': form, 'asignaturas': asignaturas}, context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def update_asignatura(request):
    """
    Modificar asignatura

    El siguiente método recoge vía request los parametros de un form,
    los evalua y modifica una asignatura si procede, en caso contrario
    deriva al template updateAsignatura.html

    :param request: request
    :return: Vista de readAsignatura.html o
            de updateAsignatura.html si algo falla
    """
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
            form = AsignaturaReadForm()
            return render_to_response('readAsignatura.html', {'form': form, 'asignaturas': asignaturas}, context)
        else:
            codigo = form.cleaned_data['codigo']
            asignatura = Asignatura.objects.get(codigo=codigo)
            return render_to_response('updateAsignatura.html', {'form': form, 'asignatura': asignatura}, context)
    id_asignatura = request.GET.get('id')
    asignatura = Asignatura.objects.get(id=id_asignatura)
    form = AsignaturaUpdateForm()
    return render_to_response('updateAsignatura.html', {'form': form, 'asignatura': asignatura}, context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def metricas(request):
    """
    Metricas de alumnos, profesores y grados

    El siguiente método calcula estadísticas para conocer
    el alumno con más reservas hechas,
    el numero de reservas totales, aceptadas y canceladas
    por los profesores y el grado con mayor alumnado

    :param request: request
    :return: Vista de miPanel o de formularioAsignatura.html si algo falla
    """
    context = RequestContext(request)

    alumnos = User.objects.filter(es_profesor=False)
    maximo = -1
    alumno_dic = {}
    for alumno in alumnos:
        num = Reserva.objects.filter(alumnos=alumno).count()
        if num > maximo:
            alumno_dic['alumno'] = alumno
            alumno_dic['num'] = num
            maximo = num

    profesores = User.objects.filter(es_profesor=True)
    profesores_dic = {}
    for profesor in profesores:
        profesor_datos = {}
        total = Reserva.objects.filter(horario__profesor=profesor).count()
        aceptadas = Reserva.objects.filter(horario__profesor=profesor).filter(estado='R').count()
        canceladas = Reserva.objects.filter(horario__profesor=profesor).filter(estado='C').count()
        profesor_datos['total'] = total
        profesor_datos['aceptadas'] = aceptadas
        profesor_datos['canceladas'] = canceladas
        profesores_dic[profesor.username] = profesor_datos

    grados = Grado.objects.all()
    maximo = -1
    grado_max = {}
    for grado in grados:
        num = User.objects.filter(usuarios=grado).count()
        if num > maximo:
            maximo = num
            grado_max['grado'] = grado
            grado_max['num'] = num
    return render_to_response('estadisticas.html', {'alumno_dic': alumno_dic,
                                                    'profesores_dic': profesores_dic,
                                                    'grado_max': grado_max}, context)

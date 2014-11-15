# encoding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from tutorias.models import *
from tutorias.form import UserForm


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect("/admin/addUser")
                elif user.es_profesor:
                    return HttpResponseRedirect("/profesor")
                else:
                    asignaturas = user.getAsignaturas()
                    return render_to_response('miPanel.html', {'asignaturas': asignaturas}, context)
            else:
                return HttpResponse("No estás activo")
        else:
            return HttpResponse("Login invalido")
    else:
        return render_to_response('index.html', {}, context)


def user_logout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


def add_users(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            print("entro")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            es_profesor = form.cleaned_data['es_profesor']
            dni = form.cleaned_data['dni']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username, email, password)
            user.es_profesor = es_profesor
            user.first_name = first_name
            user.last_name = last_name
            user.dni = dni
            user.set_password(password)

            user.save()

            return HttpResponse("PERFE")
        else:
            print("no")
    else:
        form = UserForm()
    return render_to_response('formularioUser.html', {'form': form}, context)
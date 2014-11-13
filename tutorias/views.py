#encoding:utf-8
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from tutorias.models import *

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect("/admin")
                elif user.es_profesor:
                    return HttpResponseRedirect("/profesor")
                else:
                    return HttpResponseRedirect("/")
            else:
                return HttpResponse("No estás activo")
        else:
            return HttpResponse("Login invalido")
    else:
        return render_to_response('index.html',{}, context)
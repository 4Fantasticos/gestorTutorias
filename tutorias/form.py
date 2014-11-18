#encoding:utf-8
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=50)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellidos", max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=20)
    es_profesor = forms.BooleanField(label="¿Es profesor?", initial=False, required=False)
    dni = forms.CharField(label="Dni", max_length=10)
    grado = forms.CharField(label="Grados", max_length=10)

class GradoForm(forms.Form):
    titulo = forms.CharField(label="Titulo", max_length=100)
    identificador = forms.CharField(label="Identificador", max_length=3)
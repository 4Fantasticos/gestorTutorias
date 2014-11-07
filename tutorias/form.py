from django import forms


class AlumnoForm (forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    dni = forms.CharField(max_length=9, required=True)
    usuario = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=20, required=True)
    email = forms.CharField(max_length=200, required=True)
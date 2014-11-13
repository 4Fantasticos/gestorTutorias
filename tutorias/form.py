#encoding:utf-8
from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label="Usuario",max_length=50)
    password = forms.CharField(label="Password",max_length=20)
    es_profesor = forms.BooleanField(label="¿Es profesor?",initial=False)
    dni = forms.CharField(label="Dni",max_length=10)



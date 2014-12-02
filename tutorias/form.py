# encoding:utf-8
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import ChoiceInput



class UserForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=50)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellidos", max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=20)
    es_profesor = forms.BooleanField(label="¿Es profesor?", initial=False, required=False)
    dni = forms.CharField(label="Dni", max_length=10)
    grado = forms.CharField(label="Grados", max_length=10, required=False)


class UserRemoveForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=50)


class UserReadForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=50)


class GradoForm(forms.Form):
    titulo = forms.CharField(label="Titulo", max_length=100)
    identificador = forms.CharField(label="Identificador", max_length=3)


class GradoRemoveForm(forms.Form):
    identificador = forms.CharField(label="Identificador", max_length=3)

class GradoReadForm(forms.Form):
    titulo = forms.CharField(label="Titulo", max_length=100)


DIAS_DE_LA_SEMANA = (
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
)


class HorarioForm(forms.Form):
    dia_semana = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=DIAS_DE_LA_SEMANA,
                                   label="Dia de la Semana")
    hora_inicio = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}), label="Hora")
    hora_final = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}), label="Hora")


class AsignaturaForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    codigo = forms.CharField(max_length=6)
    curso = forms.CharField(max_length=1)
    grado = forms.CharField(max_length=10)


class AsignaturaRemoveForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    grado = forms.CharField(max_length=10)


class AsignaturaRemoveForm(forms.Form):
    nombre = forms.CharField(max_length=100)


class AsignaturaReadForm(forms.Form):
    nombre = forms.CharField(max_length=100)


class AddAsignaturasForm(forms.Form):
    def __init__(self, *args, **kwargs):
        asignaturas = kwargs.pop('asignaturas')
        lista = ()
        for asig in asignaturas:
            sublista = (asig.codigo, asig.nombre)
            lista = lista + (sublista,)
        print lista
        super(AddAsignaturasForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=lista)


class AddGradosForm(forms.Form):
    def __init__(self, *args, **kwargs):
        grados = kwargs.pop('grados')
        lista = ()
        for grado in grados:
            sublista = (grado.identificador, grado.titulo)
            lista = lista + (sublista,)
        super(AddGradosForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=lista)

class AsignaturaUpdateForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    codigo = forms.CharField(max_length=6)
    curso = forms.CharField(max_length=1)

class GradoUpdateForm(forms.Form):
    titulo = forms.CharField(label="Titulo", max_length=100)
    identificador = forms.CharField(label="Identificador", max_length=3)

class UserUpdateForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=50)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellidos", max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    es_profesor = forms.BooleanField(label="¿Es profesor?", initial=False, required=False)
    dni = forms.CharField(label="Dni", max_length=10)

class ReservaTutoriasForm(forms.Form):
    mensajealumno = forms.CharField(label="mensajeAlumno",max_length=500)
    dia = forms.CharField(label="diaDelMesReseva",max_length=10)
    horario_id = forms.CharField(label="IdentificadorHorario",max_length=8)

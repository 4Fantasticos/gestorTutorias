# encoding:utf-8
from django import forms


class UserForm(forms.Form):
    """
    Formulario de Usuario
    """
    username = forms.CharField(label="Usuario", max_length=50)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellidos", max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=20)
    es_profesor = forms.BooleanField(label="¿Es profesor?", initial=False, required=False)
    dni = forms.CharField(label="Dni", max_length=10)
    grado = forms.CharField(label="Grados", max_length=10, required=False)


class UserRemoveForm(forms.Form):
    """
    Formulario para eliminar un usuario
    """
    username = forms.CharField(label="Usuario", max_length=50)


class UserReadForm(forms.Form):
    """
    Formulario para consultar un usuario
    """
    username = forms.CharField(label="Usuario", max_length=50)


class GradoForm(forms.Form):
    """
    Formulario para añadir un grado
    """
    titulo = forms.CharField(label="Titulo", max_length=100)
    identificador = forms.CharField(label="Identificador", max_length=3)


class GradoRemoveForm(forms.Form):
    """
    Formulario para eliminar un grado
    """
    identificador = forms.CharField(label="Identificador", max_length=3)


class GradoReadForm(forms.Form):
    """
    Formulario para consultar un grado
    """
    titulo = forms.CharField(label="Titulo", max_length=100)


DIAS_DE_LA_SEMANA = (
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
)


class HorarioForm(forms.Form):
    """
    Formulario para añadir un horario
    """
    dia_semana = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=DIAS_DE_LA_SEMANA,
                                   label="Dia de la Semana")
    hora_inicio = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}), label="Hora")
    hora_final = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}), label="Hora")


class AsignaturaForm(forms.Form):
    """
    Formulario para añadir una asignatura
    """
    nombre = forms.CharField(max_length=100)
    codigo = forms.CharField(max_length=6)
    curso = forms.CharField(max_length=1)
    grado = forms.CharField(max_length=10)


class AsignaturaRemoveForm(forms.Form):
    """
    Formulario para eliminar una asignatura
    """
    identificador = forms.CharField(max_length=100)


class AsignaturaReadForm(forms.Form):
    """
    Formulario para consultar una asignatura
    """
    nombre = forms.CharField(max_length=100)


class AddAsignaturasForm(forms.Form):
    """
    Formulario para añadir una asignatura a un profesor o un alumno
    """

    def __init__(self, *args, **kwargs):
        asignaturas = kwargs.pop('asignaturas')
        lista = ()
        for asig in asignaturas:
            sublista = (asig.id, asig.nombre)
            lista = lista + (sublista,)
        super(AddAsignaturasForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=lista)


class AddGradosForm(forms.Form):
    """
    Formulario para añadir grados a los profesores
    """

    def __init__(self, *args, **kwargs):
        grados = kwargs.pop('grados')
        lista = ()
        for grado in grados:
            sublista = (grado.id, grado.titulo)
            lista = lista + (sublista,)
        super(AddGradosForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=lista)


class AsignaturaUpdateForm(forms.Form):
    """
    Formulario para actualizar una asignatura
    """
    nombre = forms.CharField(max_length=100)
    codigo = forms.CharField(max_length=6)
    curso = forms.CharField(max_length=1)


class GradoUpdateForm(forms.Form):
    """
    Formulario para actualizar un grado
    """
    titulo = forms.CharField(label="Titulo", max_length=100)
    identificador = forms.CharField(label="Identificador", max_length=3)


class UserUpdateForm(forms.Form):
    """
    Formulario para actualizar un usuario
    """
    username = forms.CharField(label="Usuario", max_length=50)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellidos", max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    es_profesor = forms.BooleanField(label="¿Es profesor?", initial=False, required=False)
    dni = forms.CharField(label="Dni", max_length=10)


class ReservaTutoriasForm(forms.Form):
    """
    Formulario para reservar una tutoría
    """
    mensajealumno = forms.CharField(label="mensajeAlumno", max_length=500)
    dia = forms.CharField(label="diaDelMesReseva", max_length=10)
    horario_id = forms.CharField(label="IdentificadorHorario", max_length=8)

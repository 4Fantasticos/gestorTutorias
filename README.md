#LEEME
##Proyecto reserva horarios de tutorias

Nos hemos liado la manta a la cabeza y en lugar de elegir un proyecto sencillo sin tener que usar ningún framework, 
a nosotros se nos ocurrió que sería una buena oportunidad para aprender django.

Puede que realizar las pruebas unitarias y demás métricas de calidad sea más complicado pero somos los 4 fantasticos :D

###Requerimientos

- [Python 2.7](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/latest/installing.html)
- Django 1.7
- Dajaxice (Ajax y Django de forma facil)
- [Mixer](http://mixer.readthedocs.org/en/latest/quickstart.html) 
- virtualenv _Opcional_

###Instalación

Una vez que tengamos instalado el pip, con el siguiente comando nos descargamos el setuptools `pip install -U setuptools`. 
Después tenemos que descargarnos el entorno virtual con el comando `pip install virtualenv`.

Nos creamos una carpeta donde estará el proyecto y en la linea de comandos nos vamos al directorio y 
hacemos la creación del entorno con el comando `virtualenv proyectoCalidad`

Entramos dentro de la carpeta y después dentro de Script, ejecutamos **activate** y ya estará corriendo el entorno virtual. 
Nos vamos a la carpeta principal e instalamos django con el comando `pip install Django`

`pip install django-dajaxice`

`pip install mixer`

Hasta aquí para tener las herramientas de desarrollo, después descargar de Github el proyecto. 

###Creación del proyecto

`git clone https://github.com/4Fantasticos/gestorTutorias.git`

Si, es un clone. Basicamente porque ya lo creamos en su dia...

##Importante a realizar cuando haya un cambio en el modelo!

`python manage.py makemigrations`

`python manage.py syncdb`

##Pruebas

Para correr las pruebas en django ejecutar:

`python manage.py test`

Para testear la cobertura en django ejecutar:

`coverage run --source='.' manage.py test tutorias`

Para ver el resultado de la cobertura:

`coverage report`

Para todo lo demás `python manage.py help` ;D
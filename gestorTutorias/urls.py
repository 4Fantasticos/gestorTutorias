from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tutorias import views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'gestorTutorias.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', views.user_login, name='login'),
                       # Usuarios
                       url(r'^admin/addUser/$', views.add_users, name='add_users'),
                       url(r'^admin/removeUser/$', views.remove_user, name='remove_user'),
                       url(r'^admin/readUser/$', views.read_user, name='read_user'),
                       url(r'^admin/updateUser/$', views.update_user, name='update_user'),
                       # Grados
                       url(r'^admin/addGrado/$', views.add_grado, name='add_grado'),
                       url(r'^admin/removeGrado/$', views.remove_grado, name='remove_grado'),
                       url(r'^admin/readGrado/$', views.read_grado, name='read_grado'),
                       url(r'^admin/updateGrado/$', views.update_grado, name='update_grado'),
                       #Asignaturas
                       url(r'^admin/addAsignatura/$', views.add_asignatura, name='add_asignatura'),
                       url(r'^admin/removeAsignatura/$', views.remove_asignatura, name='remove_asignatura'),
                       url(r'^admin/readAsignatura/$', views.read_asignatura, name='read_asignatura'),
                       url(r'^admin/updateAsignatura/$', views.update_asignatura, name='update_asignatura'),
                       #Horarios
                       url(r'^admin/addHorario/$', views.add_horario, name='add_horario'),
                       url(r'^misHorarios/$', views.mis_horarios, name='misHorarios'),
                       url(r'^profesores/(?P<profesor_id>\d+)/$', views.horarios_profesores, name='hprofesor'),
                       url(r'^miPanel/reservarTutoria$', views.reservar_tutoria, name="reservar_tutoria"),
                       #Panel
                       url(r'^miPanel/$', views.miPanel, name='miPanel'),
                       url(r'^miPanel/addAsignaturasAlumno', views.addAsignaturasAlumnos,
                           name='add_asignaturas_alumno'),
                       url(r'^miPanel/addGradosProfesor', views.addGradosProfesor, name='add_grados_profesor'),
                       url(r'^miPanel/addAsignaturasProfesor', views.addAsignaturasProfesor,
                           name='add_asignaturas_profesor'),
                       url(r'^miPanel/notificaciones', views.notificacionesProfesor, name='notificaciones_profesor'),
                       #Alumnos
                       url(r'^miPanel/pedirTutoria', views.pedirTutoria, name='pedir_tutoria'),
                       #Profesor
                       url(r'^miPanel/misNotificaciones', views.notificacionesProfesor, name='mis_notificaciones'),
                       #logout
                       url(r'^logout/$', views.user_logout, name='logout'),
                       #Admin Django
                       url(r'^admin/', include(admin.site.urls)),
                       #Dataxice
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()
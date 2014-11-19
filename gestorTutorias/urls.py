from django.conf.urls import patterns, include, url
from django.contrib import admin
from tutorias import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'gestorTutorias.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^$', views.user_login, name='login'),
                       url(r'^admin/addUser/$', views.add_users, name='add_users'),
                       url(r'^admin/addGrado/$', views.add_grado, name='add_grado'),
                       url(r'^admin/addHorario/$', views.add_horario, name='add_horario'),
                       url(r'^admin/addAsignatura/$', views.add_asignatura, name='add_asignatura'),
                       url(r'^misHorarios/$', views.mis_horarios, name='misHorarios'),
                       url(r'^miPanel/$', views.miPanel, name='miPanel'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^admin/', include(admin.site.urls)),
)

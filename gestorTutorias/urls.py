from django.conf.urls import patterns, include, url
from django.contrib import admin
from tutorias import views
import tutorias

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestorTutorias.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^alumnos/', views.index),
)

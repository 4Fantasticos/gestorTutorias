from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestorTutorias.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tutorias.views.user_login', name='login'),
    url(r'^admin/addUser/$','tutorias.views.add_users',name='add_users')
)

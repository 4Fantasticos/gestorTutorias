#encoding:utf-8
from django.contrib import admin
from models import *

class AdminPersonalizado (admin.ModelAdmin):
    list_display = ('username','first_name','last_name','dni','es_profesor')
    fieldsets = (('Información principal',{'fields':('username','password','first_name','last_name','dni','email')}),
                 ('Información Secundaria',{'fields':('is_active','es_profesor','is_superuser','last_login','date_joined')}))

admin.site.unregister(User)

admin.site.register(User,AdminPersonalizado)
admin.site.register(Grado)
admin.site.register(Horario)
admin.site.register(Asignatura)
admin.site.register(Reserva)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutorias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=6)),
                ('curso', models.CharField(max_length=1)),
            ],
            options={
                'ordering': ('codigo',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('identificador', models.CharField(max_length=3)),
                ('usuarios', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('titulo',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia_semana', models.CharField(max_length=1, choices=[(b'L', b'Lunes'), (b'M', b'Martes'), (b'X', b'Miercoles'), (b'J', b'Jueves'), (b'V', b'Viernes')])),
                ('hora_inicio', models.DateTimeField()),
                ('profesor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.CharField(max_length=1, choices=[(b'R', b'Reservado'), (b'L', b'Libre'), (b'P', b'Pendiente')])),
                ('mensajeAlumno', models.CharField(max_length=500)),
                ('mensajeCancel', models.CharField(max_length=500)),
                ('dia', models.DateField()),
                ('alumnos', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('horarios', models.ManyToManyField(to='tutorias.Horario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Alumno',
        ),
        migrations.AddField(
            model_name='asignatura',
            name='grados',
            field=models.ForeignKey(to='tutorias.Grado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asignatura',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

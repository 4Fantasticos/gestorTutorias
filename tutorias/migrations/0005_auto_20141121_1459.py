# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutorias', '0004_auto_20141119_1248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asignatura',
            options={'ordering': ('curso',)},
        ),
        migrations.AlterModelOptions(
            name='horario',
            options={'ordering': ('dia_semana',)},
        ),
        migrations.AddField(
            model_name='reserva',
            name='profesor',
            field=models.ForeignKey(related_name='profesor', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='alumnos',
            field=models.ForeignKey(related_name='alumnos', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]

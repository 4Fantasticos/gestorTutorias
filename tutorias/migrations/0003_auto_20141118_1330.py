# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorias', '0002_auto_20141110_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reserva',
            options={'ordering': ('dia',)},
        ),
        migrations.AddField(
            model_name='asignatura',
            name='nombre',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='horario',
            name='dia_semana',
            field=models.CharField(max_length=1, choices=[(b'L', b'Lunes'), (b'M', b'Martes'), (b'X', b'Mi\xc3\xa9rcoles'), (b'J', b'Jueves'), (b'V', b'Viernes')]),
            preserve_default=True,
        ),
    ]

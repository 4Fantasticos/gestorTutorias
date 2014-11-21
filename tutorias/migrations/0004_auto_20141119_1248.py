# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorias', '0003_auto_20141118_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='hora_inicio',
            field=models.TimeField(),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0041_auto_20151108_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='type',
            field=models.IntegerField(null=True),
        ),
    ]

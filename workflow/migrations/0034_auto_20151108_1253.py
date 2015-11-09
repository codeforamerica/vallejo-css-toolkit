# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0033_auto_20151107_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='pge_service',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verification',
            name='water_service',
            field=models.BooleanField(default=False),
        ),
    ]

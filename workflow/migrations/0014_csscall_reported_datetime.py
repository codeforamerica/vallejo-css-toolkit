# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0013_auto_20151008_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='reported_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

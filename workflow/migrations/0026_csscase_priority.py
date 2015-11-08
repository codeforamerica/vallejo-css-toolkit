# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0025_auto_20151107_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='priority',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Low'), (2, b'Medium'), (3, b'High')]),
        ),
    ]

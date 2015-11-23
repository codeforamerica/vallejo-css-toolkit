# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0050_auto_20151115_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Unread - phone'), (1, b'Unread - web'), (3, b'Report'), (4, b'Verification'), (5, b'Resolved'), (6, b'Resolved')]),
        ),
    ]

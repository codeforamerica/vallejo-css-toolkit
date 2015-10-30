# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0021_auto_20151024_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

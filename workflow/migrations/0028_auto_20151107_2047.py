# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0027_csscase_resolved_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csscase',
            name='priority',
        ),
        migrations.AlterField(
            model_name='csscall',
            name='name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscall',
            name='problem',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]

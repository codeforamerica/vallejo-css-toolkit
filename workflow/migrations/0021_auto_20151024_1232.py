# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0020_csscase_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csscall',
            name='problem',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscall',
            name='resolution',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
    ]

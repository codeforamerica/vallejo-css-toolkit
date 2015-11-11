# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0043_auto_20151111_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='call_sid',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

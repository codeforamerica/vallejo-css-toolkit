# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0014_csscall_reported_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='tags',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

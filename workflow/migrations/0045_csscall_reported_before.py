# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0044_csscall_call_sid'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='reported_before',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

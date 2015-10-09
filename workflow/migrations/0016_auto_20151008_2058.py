# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0015_csscall_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='reporter_address_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='csscall',
            name='reporter_street_name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

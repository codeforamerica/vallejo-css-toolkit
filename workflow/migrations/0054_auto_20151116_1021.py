# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0053_auto_20151116_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csscall',
            name='report_type',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Squatters'), (2, b'Homeless encampment'), (3, b'Drugs'), (4, b'Illegal Auto Repair'), (5, b'Illegal Dumping'), (6, b'Prostitution'), (7, b'Abandoned Vehicle'), (9, b'Communication/Question'), (8, b'Other')]),
        ),
    ]

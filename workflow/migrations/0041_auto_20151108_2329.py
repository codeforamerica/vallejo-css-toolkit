# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0040_csscall_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csscall',
            name='source',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Phone'), (2, b'Email'), (3, b'Web'), (4, b'Code Enforcement Referral'), (5, b'Officer Referral'), (6, b'Other City Referral')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0004_remove_case_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='dept',
            field=models.IntegerField(null=True),
        ),
    ]

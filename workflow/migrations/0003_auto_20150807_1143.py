# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_auto_20150806_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='lng',
            field=models.FloatField(null=True),
        ),
    ]

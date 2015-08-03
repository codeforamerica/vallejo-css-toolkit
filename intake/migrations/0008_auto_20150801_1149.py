# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0007_auto_20150801_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='property_owner',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='call',
            name='property_owner_phone',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='resolution',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='caller_number',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

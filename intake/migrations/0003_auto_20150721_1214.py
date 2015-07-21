# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0002_auto_20150721_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='description_recording_url',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='problem_description',
            field=models.TextField(max_length=1024, null=True, blank=True),
        ),
    ]

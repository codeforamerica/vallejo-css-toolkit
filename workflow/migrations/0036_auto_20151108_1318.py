# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0035_auto_20151108_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='code_contacted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verification',
            name='trespass_letter',
            field=models.BooleanField(default=False),
        ),
    ]

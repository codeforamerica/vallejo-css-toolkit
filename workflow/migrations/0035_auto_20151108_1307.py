# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0034_auto_20151108_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='boarded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verification',
            name='nlp_assigned',
            field=models.BooleanField(default=False),
        ),
    ]

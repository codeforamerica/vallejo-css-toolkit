# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0024_cssreportview'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='verification',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

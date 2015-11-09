# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0036_auto_20151108_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='bank_contact',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='verification',
            name='bank_contact_phone',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='verification',
            name='bank_name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

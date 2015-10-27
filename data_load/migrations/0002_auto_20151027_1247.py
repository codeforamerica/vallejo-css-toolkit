# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_load', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rmscase',
            name='address',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='rmscase',
            name='code',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='rmscase',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='rmscase',
            name='desc',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='rmscase',
            name='incnum',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='rmscase',
            name='off_name',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]

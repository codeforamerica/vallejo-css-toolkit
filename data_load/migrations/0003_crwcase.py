# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_load', '0002_auto_20151027_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='CRWCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yr_no', models.IntegerField()),
                ('seq_no', models.IntegerField()),
                ('case_no', models.CharField(max_length=1024, null=True)),
                ('started', models.DateTimeField(null=True)),
                ('address_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=1024, null=True)),
                ('assigned_to', models.CharField(max_length=1024, null=True)),
                ('status', models.CharField(max_length=1024, null=True)),
                ('desc', models.CharField(max_length=1024, null=True)),
                ('case_type', models.CharField(max_length=1024, null=True)),
                ('case_subtype', models.CharField(max_length=1024, null=True)),
            ],
        ),
    ]

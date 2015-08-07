# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=256, null=True)),
                ('street_descriptor', models.CharField(max_length=256, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('call_sid', models.CharField(max_length=256, null=True)),
                ('caller_name', models.CharField(max_length=256, null=True)),
                ('name_recording_url', models.CharField(max_length=256, null=True)),
                ('caller_number', models.BigIntegerField(null=True)),
                ('call_time', models.DateTimeField(auto_now_add=True)),
                ('caller_preferred_contact', models.IntegerField(null=True)),
                ('problem_address', models.CharField(max_length=256, null=True)),
                ('address_recording_url', models.CharField(max_length=256, null=True)),
                ('problem_description', models.CharField(max_length=1024, null=True)),
                ('description_recording_url', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]

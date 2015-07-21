# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='address_recording_url',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='caller_name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='caller_number',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='caller_preferred_contact',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='description_recording_url',
            field=models.TextField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='name_recording_url',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='problem_address',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='problem_description',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
    ]

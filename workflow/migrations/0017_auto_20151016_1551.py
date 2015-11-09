# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0016_auto_20151008_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscall',
            name='num_people_involved',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='csscall',
            name='problem_duration',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='csscall',
            name='reporter_alternate_contact',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='csscall',
            name='safety_concerns',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='csscall',
            name='time_of_day_occurs',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='csscall',
            name='when_last_reported',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

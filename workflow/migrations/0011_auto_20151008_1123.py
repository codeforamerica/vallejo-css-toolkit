# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0010_auto_20151008_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecordingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='csscall',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='assignee',
        ),
        migrations.AddField(
            model_name='csscall',
            name='place_name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='call',
            field=models.ForeignKey(to='workflow.CSSCall'),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_type',
            field=models.ForeignKey(to='workflow.RecordingType'),
        ),
    ]

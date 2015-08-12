# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='CSSCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('resolution', models.CharField(max_length=1024, null=True)),
                ('raw_address', models.CharField(max_length=256, null=True)),
                ('status', models.ForeignKey(to='workflow.CaseStatus', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PDCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('raw_address', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]

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
            name='CRWCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CSSCall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, null=True)),
                ('address', models.CharField(max_length=256, null=True, blank=True)),
                ('phone', models.CharField(max_length=256, null=True, blank=True)),
                ('problem', models.CharField(max_length=256, null=True, blank=True)),
                ('date', models.CharField(max_length=256, null=True, blank=True)),
                ('resolution', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CSSCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('resolution', models.CharField(max_length=1024, null=True)),
                ('address_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=256, null=True)),
                ('status', models.ForeignKey(to='workflow.CaseStatus', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PDCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
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
        migrations.RenameField(
            model_name='csscase',
            old_name='raw_address',
            new_name='street_name',
        ),
        migrations.RenameField(
            model_name='pdcase',
            old_name='raw_address',
            new_name='street_name',
        ),
        migrations.AddField(
            model_name='csscase',
            name='address_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pdcase',
            name='address_number',
            field=models.IntegerField(null=True),
        ),
    ]

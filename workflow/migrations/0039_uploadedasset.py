# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0038_verificationcontactaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(max_length=256, null=True, blank=True)),
                ('fpath', models.CharField(max_length=256, null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('verification', models.ForeignKey(to='workflow.Verification')),
            ],
        ),
    ]

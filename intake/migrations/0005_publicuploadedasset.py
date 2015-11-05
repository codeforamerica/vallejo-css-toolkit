# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0023_csscall_caller_preferred_contact'),
        ('intake', '0004_auto_20151105_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicUploadedAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fpath', models.CharField(max_length=256, null=True, blank=True)),
                ('css_report', models.ForeignKey(to='workflow.CSSCall')),
            ],
        ),
    ]

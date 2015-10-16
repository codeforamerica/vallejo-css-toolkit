# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0017_auto_20151016_1551'),
        ('intake', '0002_typeformsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeformAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_url', models.CharField(max_length=256, null=True, blank=True)),
                ('css_report', models.ForeignKey(to='workflow.CSSCall')),
            ],
        ),
    ]

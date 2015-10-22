# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0017_auto_20151016_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('property_desciption', models.CharField(max_length=256, null=True, blank=True)),
                ('owner_name', models.CharField(max_length=256, null=True, blank=True)),
                ('owner_address', models.CharField(max_length=256, null=True, blank=True)),
                ('owner_primary_contact', models.CharField(max_length=256, null=True, blank=True)),
                ('owner_secondary_contact', models.CharField(max_length=256, null=True, blank=True)),
                ('report', models.ForeignKey(to='workflow.CSSCall')),
            ],
        ),
    ]

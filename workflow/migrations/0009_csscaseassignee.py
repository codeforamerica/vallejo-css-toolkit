# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0008_auto_20150930_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSCaseAssignee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignee_name', models.CharField(max_length=256, null=True, blank=True)),
                ('case', models.ForeignKey(blank=True, to='workflow.CSSCase', null=True)),
            ],
        ),
    ]

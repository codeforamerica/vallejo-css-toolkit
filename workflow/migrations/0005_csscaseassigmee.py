# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0004_auto_20150921_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSCaseAssigmee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignee_name', models.CharField(max_length=256, null=True, blank=True)),
                ('case', models.ForeignKey(blank=True, to='workflow.CaseStatus', null=True)),
            ],
        ),
    ]

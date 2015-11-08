# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0030_auto_20151107_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='csscall',
            name='status',
            field=models.ForeignKey(blank=True, to='workflow.ReportStatus', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0031_auto_20151107_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField()),
                ('sent_at', models.DateTimeField(null=True)),
                ('report', models.ForeignKey(to='workflow.CSSCall')),
            ],
        ),
    ]

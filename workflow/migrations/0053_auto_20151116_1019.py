# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0052_csscall_report_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='case_no',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscall',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Unread - phone'), (1, b'Unread - web'), (3, b'Report'), (4, b'Verification'), (5, b'Case'), (6, b'Resolved')]),
        ),
    ]

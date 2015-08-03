# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0008_auto_20150801_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='call_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Unreviewed'), (2, b'Active'), (3, b'Closed'), (4, b'Suspended')]),
        ),
    ]

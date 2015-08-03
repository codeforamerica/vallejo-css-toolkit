# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0005_auto_20150731_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='caller_preferred_contact',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'None'), (1, b'Text'), (3, b'Call')]),
        ),
    ]

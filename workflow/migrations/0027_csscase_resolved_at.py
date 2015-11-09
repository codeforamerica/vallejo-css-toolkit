# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0026_csscase_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='resolved_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

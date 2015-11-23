# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0049_csscase_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csscall',
            name='status',
        ),
        migrations.DeleteModel(
            name='ReportStatus',
        ),
    ]

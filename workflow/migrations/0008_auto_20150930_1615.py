# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0007_csscaseassignee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csscaseassignee',
            name='case',
        ),
        migrations.DeleteModel(
            name='CSSCaseAssignee',
        ),
    ]

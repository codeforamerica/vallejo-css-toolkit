# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0005_csscaseassigmee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csscaseassigmee',
            name='case',
        ),
        migrations.DeleteModel(
            name='CSSCaseAssigmee',
        ),
    ]

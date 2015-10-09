# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0012_csscasecall'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csscasecall',
            name='call',
        ),
        migrations.RemoveField(
            model_name='csscasecall',
            name='case',
        ),
        migrations.DeleteModel(
            name='CSSCaseCall',
        ),
    ]

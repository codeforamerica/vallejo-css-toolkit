# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_auto_20150807_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='address',
        ),
    ]

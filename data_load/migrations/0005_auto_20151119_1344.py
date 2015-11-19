# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_load', '0004_rmsinciden'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RMSInciden',
            new_name='RMSIncident',
        ),
    ]

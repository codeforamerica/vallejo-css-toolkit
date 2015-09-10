# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationposition',
            old_name='street_number',
            new_name='address_number',
        ),
        migrations.RemoveField(
            model_name='locationposition',
            name='street_descriptor',
        ),
    ]

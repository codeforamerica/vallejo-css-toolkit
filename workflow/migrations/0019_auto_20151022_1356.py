# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0018_verification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verification',
            old_name='property_desciption',
            new_name='property_description',
        ),
    ]

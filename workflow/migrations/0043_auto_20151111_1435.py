# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0042_recording_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recording',
            name='recording_type',
        ),
        migrations.DeleteModel(
            name='RecordingType',
        ),
    ]

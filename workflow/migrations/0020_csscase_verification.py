# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0019_auto_20151022_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='verification',
            field=models.ForeignKey(default=1, to='workflow.Verification'),
            preserve_default=False,
        ),
    ]

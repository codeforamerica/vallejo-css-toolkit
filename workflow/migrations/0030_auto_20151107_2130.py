# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0029_auto_20151107_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csscase',
            name='verification',
            field=models.ForeignKey(to='workflow.Verification', null=True),
        ),
    ]

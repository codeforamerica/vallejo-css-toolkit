# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0032_reportnotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportnotification',
            name='message',
            field=models.CharField(max_length=512),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_csscall_assignee'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='owner_address',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='csscase',
            name='owner_email',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='csscase',
            name='owner_name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='csscase',
            name='owner_phone',
            field=models.CharField(max_length=256, null=True),
        ),
    ]

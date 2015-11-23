# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0047_caseaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csscase',
            name='address_number',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='owner_address',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='owner_email',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='owner_name',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='owner_phone',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='status',
        ),
        migrations.RemoveField(
            model_name='csscase',
            name='street_name',
        ),
        migrations.DeleteModel(
            name='CSSCasePriority',
        ),
    ]

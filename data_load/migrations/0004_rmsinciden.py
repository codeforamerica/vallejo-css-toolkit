# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_load', '0003_crwcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='RMSInciden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('incident_no', models.BigIntegerField()),
            ],
        ),
    ]

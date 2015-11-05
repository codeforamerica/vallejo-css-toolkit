# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0003_typeformasset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='caller_preferred_contact',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'No Contact'), (1, b'Text'), (3, b'Call'), (4, b'Email')]),
        ),
    ]

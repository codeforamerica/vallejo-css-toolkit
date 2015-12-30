# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0058_caseview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseview',
            name='case',
            field=models.ForeignKey(to='workflow.CSSCase'),
        ),
    ]

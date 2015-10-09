# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0011_auto_20151008_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSCaseCall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('call', models.ForeignKey(to='workflow.CSSCall')),
                ('case', models.ForeignKey(to='workflow.CSSCase')),
            ],
        ),
    ]

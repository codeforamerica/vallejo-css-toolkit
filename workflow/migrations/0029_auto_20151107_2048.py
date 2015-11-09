# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0028_auto_20151107_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSCasePriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='csscase',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='csscase',
            name='priority',
            field=models.ForeignKey(blank=True, to='workflow.CSSCasePriority', null=True),
        ),
    ]

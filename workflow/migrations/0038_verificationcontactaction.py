# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0037_auto_20151108_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationContactAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contacter_name', models.CharField(max_length=256, null=True, blank=True)),
                ('contact_type', models.CharField(max_length=256, null=True, blank=True)),
                ('contact_description', models.CharField(max_length=256, null=True, blank=True)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
                ('verification', models.ForeignKey(to='workflow.Verification')),
            ],
        ),
    ]

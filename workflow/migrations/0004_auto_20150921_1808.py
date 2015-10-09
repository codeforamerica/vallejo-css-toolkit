# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0003_auto_20150921_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscase',
            name='assignee',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='address_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='description',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='owner_address',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='owner_email',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='owner_name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='owner_phone',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='resolution',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='status',
            field=models.ForeignKey(blank=True, to='workflow.CaseStatus', null=True),
        ),
        migrations.AlterField(
            model_name='csscase',
            name='street_name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]

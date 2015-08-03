# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('intake', '0006_auto_20150731_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callassignment',
            name='call',
        ),
        migrations.RemoveField(
            model_name='callassignment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='call',
            name='active',
        ),
        migrations.RemoveField(
            model_name='call',
            name='is_duplicate',
        ),
        migrations.RemoveField(
            model_name='call',
            name='is_reviewed',
        ),
        migrations.AddField(
            model_name='call',
            name='assignee',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='call',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Unreviwed'), (2, b'Active'), (3, b'Closed'), (4, b'Suspended')]),
        ),
        migrations.AlterField(
            model_name='call',
            name='caller_preferred_contact',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'No Contact'), (1, b'Text'), (3, b'Call')]),
        ),
        migrations.DeleteModel(
            name='CallAssignment',
        ),
    ]

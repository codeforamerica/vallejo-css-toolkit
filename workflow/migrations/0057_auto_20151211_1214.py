# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0056_verificationview'),
    ]

    operations = [
        migrations.AddField(
            model_name='csscaseassignee',
            name='assignee_user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffreportnotification',
            name='from_user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

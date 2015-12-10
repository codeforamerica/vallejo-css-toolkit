# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0054_auto_20151116_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffReportNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField()),
                ('sent_at', models.DateTimeField(null=True)),
                ('from_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('report', models.ForeignKey(to='workflow.CSSCall')),
                ('to_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

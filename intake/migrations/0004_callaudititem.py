# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('intake', '0003_auto_20150721_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallAuditItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('changed_field', models.CharField(max_length=256, null=True, blank=True)),
                ('old_value', models.CharField(max_length=256, null=True, blank=True)),
                ('new_value', models.CharField(max_length=256, null=True, blank=True)),
                ('call', models.ForeignKey(to='intake.Call')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

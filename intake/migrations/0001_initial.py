# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('call_sid', models.CharField(max_length=256, null=True)),
                ('caller_name', models.CharField(max_length=256, null=True, blank=True)),
                ('name_recording_url', models.CharField(max_length=256, null=True, blank=True)),
                ('caller_number', models.CharField(max_length=256, null=True, blank=True)),
                ('call_time', models.DateTimeField(null=True)),
                ('caller_preferred_contact', models.IntegerField(blank=True, null=True, choices=[(1, b'No Contact'), (1, b'Text'), (3, b'Call')])),
                ('problem_address', models.CharField(max_length=256, null=True, blank=True)),
                ('address_recording_url', models.CharField(max_length=256, null=True, blank=True)),
                ('problem_description', models.TextField(max_length=1024, null=True, blank=True)),
                ('description_recording_url', models.CharField(max_length=256, null=True, blank=True)),
                ('resolution', models.CharField(max_length=256, null=True, blank=True)),
                ('status', models.IntegerField(blank=True, null=True, choices=[(1, b'Unreviewed'), (2, b'Active'), (3, b'Closed'), (4, b'Suspended')])),
                ('property_owner', models.CharField(max_length=256, null=True, blank=True)),
                ('property_owner_phone', models.BigIntegerField(null=True, blank=True)),
                ('assignee', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
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
